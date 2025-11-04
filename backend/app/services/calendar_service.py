from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class CalendarService:
    """
    Google Calendar integration
    Handles reading and managing calendar events
    """

    def __init__(self, credentials: Credentials):
        self.service = build("calendar", "v3", credentials=credentials)

    async def get_today_events(self) -> List[Dict]:
        """Get all events for today"""
        try:
            now = datetime.utcnow()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=start_of_day.isoformat() + "Z",
                    timeMax=end_of_day.isoformat() + "Z",
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            return [
                {
                    "id": event["id"],
                    "summary": event.get("summary", "Event"),
                    "start": event["start"].get("dateTime", event["start"].get("date")),
                    "end": event["end"].get("dateTime", event["end"].get("date")),
                    "description": event.get("description", ""),
                }
                for event in events
            ]

        except Exception as e:
            print(f"Error fetching calendar events: {e}")
            return []

    async def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Get events for the next N days"""
        try:
            now = datetime.utcnow()
            future = now + timedelta(days=days)

            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now.isoformat() + "Z",
                    timeMax=future.isoformat() + "Z",
                    maxResults=50,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            return [
                {
                    "id": event["id"],
                    "summary": event.get("summary", "Event"),
                    "start": event["start"].get("dateTime", event["start"].get("date")),
                    "end": event["end"].get("dateTime", event["end"].get("date")),
                    "description": event.get("description", ""),
                }
                for event in events
            ]

        except Exception as e:
            print(f"Error fetching upcoming events: {e}")
            return []

    async def create_reminder(
        self, summary: str, start_time: datetime, duration_minutes: int = 60
    ) -> Optional[Dict]:
        """Create a calendar reminder (requires user confirmation)"""
        try:
            end_time = start_time + timedelta(minutes=duration_minutes)

            event = {
                "summary": summary,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "America/Denver",  # TODO: Make this user-configurable
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "America/Denver",
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 15},
                        {"method": "popup", "minutes": 60},
                    ],
                },
            }

            created_event = (
                self.service.events().insert(calendarId="primary", body=event).execute()
            )

            return {
                "id": created_event["id"],
                "summary": created_event.get("summary"),
                "start": created_event["start"].get("dateTime"),
                "link": created_event.get("htmlLink"),
            }

        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return None

    def format_for_speech(self, events: List[Dict]) -> str:
        """Format events for voice response"""
        if not events:
            return "You don't have any events scheduled."

        count = len(events)
        speech = f"You have {count} event{'s' if count > 1 else ''} today. "

        for i, event in enumerate(events[:3]):  # Only mention first 3
            summary = event["summary"]
            start = event["start"]

            # Parse time
            try:
                if "T" in start:  # DateTime format
                    dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                    time_str = dt.strftime("%I:%M %p")
                else:  # Date only (all day event)
                    time_str = "all day"
            except:
                time_str = ""

            speech += f"{summary}"
            if time_str:
                speech += f" at {time_str}"

            if i < len(events) - 1:
                speech += ", "

        if count > 3:
            speech += f", and {count - 3} more events."

        return speech
