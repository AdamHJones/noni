from anthropic import Anthropic
from typing import Dict, List, Optional
import base64
import json
from app.core.config import settings


class VisionService:
    """
    Claude Vision API integration for extracting information from photos
    Handles: prescriptions, medication labels, doctor notes, recipes, food labels, signs
    """

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def analyze_image(
        self,
        image_data: str,
        analysis_type: str,
        user_medications: Optional[List[Dict]] = None,
    ) -> Dict:
        """
        Analyze an image using Claude's vision capabilities

        Args:
            image_data: Base64 encoded image data (with data:image prefix)
            analysis_type: Type of analysis (prescription, medication, etc.)
            user_medications: Current medications for interaction checking

        Returns:
            Dict with analysis results, warnings, and suggestions
        """

        # Remove data URL prefix if present
        if "," in image_data:
            image_data = image_data.split(",")[1]

        # Build prompt based on analysis type
        prompt = self._build_prompt(analysis_type, user_medications)

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data,
                                },
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )

            # Parse response
            analysis_text = response.content[0].text

            # Extract structured data based on type
            result = self._parse_analysis(analysis_text, analysis_type, user_medications)

            return {
                "success": True,
                "analysis": result["analysis"],
                "warnings": result.get("warnings", []),
                "suggestions": result.get("suggestions", []),
                "extracted_data": result.get("extracted_data"),
            }

        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {
                "success": False,
                "analysis": "I had trouble reading this image. Please try again with better lighting or a clearer photo.",
                "warnings": [str(e)],
            }

    def _build_prompt(
        self, analysis_type: str, user_medications: Optional[List[Dict]]
    ) -> str:
        """Build appropriate prompt for the analysis type"""

        base_instructions = """You are helping an elderly person with Alzheimer's disease.
Your analysis should be:
- Clear and simple (5th grade reading level)
- Compassionate and patient
- Focused on safety
- Highlighting important information only"""

        type_prompts = {
            "prescription": f"""{base_instructions}

This is a prescription. Please extract and explain:

1. **Medication name** (generic and brand if shown)
2. **Dosage** (how much to take)
3. **Frequency** (how often to take it)
4. **Special instructions** (with food, at bedtime, etc.)
5. **Prescribing doctor**
6. **Refill information**

IMPORTANT: Check for interactions with current medications: {self._format_medications(user_medications)}

Format your response clearly with:
- WHAT IT IS: [medication name and purpose]
- HOW TO TAKE IT: [simple instructions]
- WARNINGS: [any important safety info or interactions]
- WHAT TO DO: [next steps]""",
            "medication": f"""{base_instructions}

This is a medication label. Please extract:

1. **Drug name** (active ingredient)
2. **Dosage strength**
3. **How to take it** (instructions)
4. **Warnings** (side effects, precautions)
5. **Expiration date**
6. **Storage instructions**

Check for interactions with: {self._format_medications(user_medications)}

Explain in simple terms what this medication is for and how to use it safely.""",
            "doctor_note": f"""{base_instructions}

This is a doctor's note. Please:

1. Summarize the main points in simple language
2. Extract any diagnoses mentioned
3. List any new medications or treatments
4. Note any follow-up appointments or tests needed
5. Highlight anything urgent or important

Present this information clearly so the patient and caregiver can understand next steps.""",
            "recipe": f"""{base_instructions}

This is a recipe. Please extract:

1. **Recipe name**
2. **Ingredients** (with amounts)
3. **Steps** (numbered, simplified)
4. **Cooking time**
5. **Servings**

IMPORTANT: Check ingredients against dietary restrictions or medication interactions: {self._format_medications(user_medications)}

Simplify the instructions and highlight any potential allergens or concerning ingredients.""",
            "food_label": f"""{base_instructions}

This is a food label. Please extract:

1. **Product name**
2. **Key ingredients** (first 5)
3. **Allergen warnings**
4. **Nutritional highlights** (calories, sodium, sugar)
5. **Serving size**

Check for:
- Allergens
- High sodium (concern for blood pressure)
- High sugar (concern for diabetes)
- Interactions with medications: {self._format_medications(user_medications)}

Explain if this food is safe to eat based on common elderly health concerns.""",
            "nutrition": f"""{base_instructions}

This is nutrition information. Please explain:

1. **Calories per serving**
2. **Sodium** (highlight if high - over 400mg)
3. **Sugar** (highlight if high - over 15g)
4. **Protein**
5. **Key vitamins/minerals**

Check against common dietary restrictions for elderly:
- Low sodium (heart health)
- Low sugar (diabetes)
- Adequate protein

Current medications: {self._format_medications(user_medications)}

Explain in simple terms if this is a healthy choice.""",
            "sign": f"""{base_instructions}

Please read this sign or text and:

1. **Read the text exactly as written**
2. **Explain what it means** in simple language
3. **Highlight important information** (warnings, directions, instructions)
4. **Suggest what to do** if it's instructional

Make it very clear what this sign is telling the person to do.""",
        }

        return type_prompts.get(
            analysis_type,
            f"{base_instructions}\n\nPlease read and explain what you see in this image in simple, clear language.",
        )

    def _format_medications(self, medications: Optional[List[Dict]]) -> str:
        """Format current medications for prompt"""
        if not medications:
            return "No current medications listed"

        med_list = []
        for med in medications:
            med_list.append(f"{med.get('name')} {med.get('dosage', '')}")

        return ", ".join(med_list)

    def _parse_analysis(
        self, analysis_text: str, analysis_type: str, user_medications: Optional[List[Dict]]
    ) -> Dict:
        """Parse Claude's response into structured format"""

        # Extract warnings (look for keywords)
        warnings = []
        warning_keywords = [
            "WARNING",
            "CAUTION",
            "DO NOT",
            "DANGER",
            "interaction",
            "contraindication",
            "allergy",
            "side effect",
        ]

        lines = analysis_text.split("\n")
        for line in lines:
            if any(keyword.lower() in line.lower() for keyword in warning_keywords):
                warnings.append(line.strip("*- "))

        # Extract suggestions
        suggestions = []
        suggestion_keywords = [
            "WHAT TO DO",
            "RECOMMEND",
            "SUGGEST",
            "SHOULD",
            "CONSIDER",
            "next step",
        ]

        for line in lines:
            if any(keyword.lower() in line.lower() for keyword in suggestion_keywords):
                suggestions.append(line.strip("*- "))

        # Try to extract structured data for medications
        extracted_data = None
        if analysis_type in ["prescription", "medication"]:
            extracted_data = self._extract_medication_data(analysis_text)

        return {
            "analysis": analysis_text,
            "warnings": warnings if warnings else None,
            "suggestions": suggestions if suggestions else None,
            "extracted_data": extracted_data,
        }

    def _extract_medication_data(self, text: str) -> Optional[Dict]:
        """Extract structured medication data from analysis"""
        # This is a simple extraction - Claude's response is already pretty structured
        # In production, you might use more sophisticated parsing

        data = {}

        # Look for common patterns
        patterns = {
            "name": ["medication name", "drug name", "what it is"],
            "dosage": ["dosage", "dose", "strength"],
            "frequency": ["frequency", "how often", "take"],
            "instructions": ["instructions", "how to take"],
        }

        lines = text.lower().split("\n")
        for key, keywords in patterns.items():
            for line in lines:
                if any(kw in line for kw in keywords):
                    # Extract value after colon if present
                    if ":" in line:
                        value = line.split(":", 1)[1].strip()
                        data[key] = value
                        break

        return data if data else None

    async def check_medication_interactions(
        self, new_medication: str, current_medications: List[Dict]
    ) -> Dict:
        """
        Check for potential drug interactions

        Args:
            new_medication: New medication to check
            current_medications: List of current medications

        Returns:
            Dict with interaction warnings and recommendations
        """

        if not current_medications:
            return {
                "interactions": [],
                "warnings": [],
                "safe": True,
            }

        current_meds_str = self._format_medications(current_medications)

        prompt = f"""You are a medication safety assistant.

NEW MEDICATION: {new_medication}

CURRENT MEDICATIONS: {current_meds_str}

Please check for:
1. Drug-drug interactions
2. Duplicate medications (same class)
3. Concerning combinations

Provide:
- List of interactions (if any)
- Severity level (mild, moderate, severe)
- What could happen
- What to do (talk to doctor, etc.)

Be clear and specific. This is for an elderly person with Alzheimer's, so explain simply."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            analysis = response.content[0].text

            # Parse for severity
            severe = any(
                word in analysis.lower()
                for word in ["severe", "dangerous", "contraindicated", "do not"]
            )

            return {
                "interactions": [analysis],
                "warnings": [analysis] if severe else [],
                "safe": not severe,
                "recommendation": "Please consult with your doctor before taking this medication."
                if severe
                else "This appears safe, but verify with your pharmacist.",
            }

        except Exception as e:
            print(f"Error checking interactions: {e}")
            return {
                "interactions": [],
                "warnings": [
                    "Could not check interactions. Please consult your doctor or pharmacist."
                ],
                "safe": False,  # Err on the side of caution
            }


# Singleton instance
vision_service = VisionService()
