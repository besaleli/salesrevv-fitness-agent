"""NeetoCal integration."""
from typing import List
import asyncio
from datetime import datetime
import aiohttp
from pydantic import BaseModel, ConfigDict, PrivateAttr
from ..env_settings import NEETOCAL_API_KEY, NEETOCAL_WORKSPACE, NEETOCAL_MEETING_SLUG

def construct_session() -> aiohttp.ClientSession:
    """Construct session."""
    return aiohttp.ClientSession(
        f"https://{NEETOCAL_WORKSPACE}.neetocal.com",
        headers={"X-Api-Key": NEETOCAL_API_KEY}
        )


class NeetoCalSlot(BaseModel):
    """NeetoCal Slot."""
    start_time: datetime
    end_time: datetime
    member_availability: dict

    def prettyprint(self) -> str:
        """Prettyprint."""
        members = ", ".join(self.member_availability.keys())
        start_time_formatted = self.start_time.strftime("%A, %b %d %Y, %H:%M")
        end_time_formatted = self.end_time.strftime("%H:%M")
        return f"Meeting with {members} from {start_time_formatted} to {end_time_formatted}"

    @classmethod
    async def new(cls, date: str, timeslot: str, member_availability: dict) -> "NeetoCalSlot":
        """Create new NeetoCalSlot.

        Args:
            date (str): Date in YYYY-MM-DD format.
            timeslot (str): Time slot in HH:MM-HH:MM format.
            member_availability (dict): Member availability.

        Returns:
            NeetoCalSlot: NeetoCalSlot.
        """
        # Split the timeslot into start and end times
        start_str, end_str = timeslot.split('-')

        # Parse the start and end times
        start_time_str = f"{date} {start_str}"
        end_time_str = f"{date} {end_str}"

        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')

        # Create and return the NeetoCalSlot instance
        return cls(
            start_time=start_time,
            end_time=end_time,
            member_availability=member_availability
            )


class NeetoCalHandler(BaseModel):
    """NeetoCal Handler."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _session: aiohttp.ClientSession = PrivateAttr(default_factory=construct_session)
    meeting_slug: str = NEETOCAL_MEETING_SLUG

    async def available_slots(
        self,
        month: int,
        year: int,
        timezone: str = 'America/New_York'
        ) -> List[NeetoCalSlot]:
        """Available slots."""
        data = {
            'month': month,
            'year': year,
            'time_zone': timezone
        }

        available_slots: List[NeetoCalSlot] = []

        async with self._session.get(
            f"/api/external/v1/slots/{self.meeting_slug}",
            json=data
            ) as response:
            response.raise_for_status()
            for slot in (await response.json())["slots"]:
                date = slot["date"]
                slots = await asyncio.gather(
                    *[
                        NeetoCalSlot.new(
                            date=date,
                            timeslot=timeslot,
                            member_availability=timeslot_data["member_availability"]
                        ) for timeslot, timeslot_data in dict(slot["slots"]).items()
                    ]
                )

                available_slots.extend(slots)

        return available_slots
