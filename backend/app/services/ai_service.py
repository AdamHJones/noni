from anthropic import Anthropic
from typing import List, Dict, Optional
from app.core.config import settings


class AIAssistant:
    """
    AI-native assistant powered by Claude
    Handles all conversational interactions with empathy and patience
    """

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt for Claude"""
        return """You are a caring AI assistant for an elderly person with Alzheimer's disease and dementia.

CRITICAL GUIDELINES:
- Be patient, warm, and never condescending
- Use simple, clear language (5th grade reading level)
- Repeat information naturally if asked again - NEVER show frustration
- Speak in short, clear sentences
- Avoid complex concepts or jargon
- Always confirm understanding
- Offer reassurance and comfort
- Remember: dignity and respect are paramount

PERSONALITY:
- Warm and friendly, like a caring family member
- Patient and understanding
- Never frustrated by repetition
- Gentle with corrections
- Encouraging and positive

SAFETY RULES:
- Never agree to send money or make purchases without caregiver approval
- Always require confirmation for any action
- If user seems distressed, offer to contact caregiver
- Watch for emergency keywords: help, hurt, fell, lost, scared, confused
- Never provide medical advice (only reminders about medications)

RESPONSE STYLE:
- Start with acknowledgment ("I understand", "Let me help you")
- Keep sentences under 15 words
- Use the person's name occasionally
- Acknowledge feelings ("I can see that's concerning")
- Offer simple choices when appropriate
- End with an offer to help more

AVAILABLE CAPABILITIES:
- Check calendar and appointments
- Read messages and emails
- Check bank balance (read-only)
- Remind about medications
- Contact caregivers
- Set reminders
- Answer questions about daily schedule

IMPORTANT: If asked the same question multiple times, respond warmly each time.
Example: "As I mentioned earlier, your appointment is at 2pm. That's in about 3 hours. Would you like me to remind you again closer to the time?"

Remember: This person may be confused, scared, or forgetful. Your job is to provide comfort, clarity, and safety."""

    async def chat(
        self,
        user_message: str,
        conversation_history: List[Dict],
        context: Optional[Dict] = None,
    ) -> Dict:
        """
        Process a user message and return AI response

        Args:
            user_message: The user's input
            conversation_history: Previous conversation messages
            context: Additional context (calendar, medications, etc.)

        Returns:
            Dict with response text and any suggested actions
        """

        # Build context prompt if provided
        context_info = ""
        if context:
            context_info = self._format_context(context)

        # Prepare messages for Claude
        messages = conversation_history.copy()

        # Add current message with context
        current_message = user_message
        if context_info:
            current_message = f"{context_info}\n\nUser says: {user_message}"

        messages.append({"role": "user", "content": current_message})

        # Call Claude API
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                temperature=0.7,
                system=self.system_prompt,
                messages=messages,
            )

            assistant_message = response.content[0].text

            # Analyze response for actions
            suggested_action = self._extract_action(assistant_message, user_message)

            return {
                "response": assistant_message,
                "suggested_action": suggested_action,
                "needs_confirmation": suggested_action is not None,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
            }

        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return {
                "response": "I'm sorry, I'm having trouble right now. Can you try asking again in a moment?",
                "error": str(e),
                "suggested_action": None,
                "needs_confirmation": False,
            }

    def _format_context(self, context: Dict) -> str:
        """Format context information for Claude"""
        parts = ["[CONTEXT - Information available to help the user]"]

        if context.get("calendar_today"):
            events = context["calendar_today"]
            if events:
                parts.append(
                    f"Today's calendar: {', '.join([e.get('summary', 'Event') for e in events])}"
                )
            else:
                parts.append("Today's calendar: No events scheduled")

        if context.get("medications_due"):
            meds = context["medications_due"]
            if meds:
                parts.append(
                    f"Medications due now: {', '.join([m.get('name', 'Medication') for m in meds])}"
                )

        if context.get("account_balance"):
            parts.append(f"Bank account balance: ${context['account_balance']:,.2f}")

        if context.get("unread_messages"):
            count = context["unread_messages"]
            parts.append(f"Unread messages: {count}")

        if context.get("user_name"):
            parts.append(f"User's name: {context['user_name']}")

        if context.get("current_time"):
            parts.append(f"Current time: {context['current_time']}")

        parts.append("[END CONTEXT]\n")

        return "\n".join(parts)

    def _extract_action(self, response: str, user_message: str) -> Optional[Dict]:
        """
        Extract suggested action from response

        Returns structured action if detected, None otherwise
        """
        response_lower = response.lower()
        user_lower = user_message.lower()

        # Detect communication actions
        if any(word in user_lower for word in ["text", "send message", "message"]):
            return {
                "type": "send_message",
                "requires_approval": "caregiver",
                "confirmation_needed": True,
            }

        if any(word in user_lower for word in ["call", "phone"]):
            return {
                "type": "make_call",
                "requires_approval": "user",
                "confirmation_needed": True,
            }

        # Detect scheduling actions
        if any(word in user_lower for word in ["schedule", "appointment", "remind me"]):
            return {
                "type": "create_reminder",
                "requires_approval": "user",
                "confirmation_needed": True,
            }

        # Detect emergency situations
        if any(
            word in user_lower for word in ["help", "emergency", "hurt", "fell", "scared"]
        ):
            return {
                "type": "emergency_alert",
                "requires_approval": None,  # Auto-execute
                "confirmation_needed": False,
            }

        return None

    def format_for_speech(self, text: str) -> str:
        """
        Format text for text-to-speech
        (Add pauses, emphasis, etc.)
        """
        # Add natural pauses
        text = text.replace(". ", "... ")
        text = text.replace("? ", "?... ")

        # Slow down for important info
        if "appointment" in text.lower():
            text = text.replace("appointment", "... appointment ...")

        return text


# Singleton instance
ai_assistant = AIAssistant()
