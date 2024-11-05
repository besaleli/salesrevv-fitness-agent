"""Tools."""
from typing import List
from ..integrations.neetocal import NeetoCalHandler

LIST_AVAILABLE_SLOTS = {
    'type': 'function',
    'function': {
        'name': 'list_available_slots',
        'description': 'List available appointment slots for personal trainer in a given month.',
        'parameters': {
            'type': 'object',
            'properties': {
                'month': {
                    'type': 'integer',
                    'description': 'Appointment month.'
                },
                'year': {
                    'type': 'integer',
                    'description': 'Appointment year.'
                },
            }
        }
    },
}

BOOK_APPOINTMENT = {
    'type': 'function',
    'function': {
        'name': 'book_appointment',
        'description': 'Book appointment with personal trainer.',
        'parameters': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'Client name.'
                },
                'email': {
                    'type': 'string',
                    'description': 'Client email.'
                },
                'slot_date': {
                    'type': 'string',
                    'description': 'Slot date. Format: YYYY-MM-DD'
                },
                'slot_start_time': {
                    'type': 'string',
                    'description': 'Slot start time. Format: HH:MM AM/PM'
                }
            }
        }
    },
}

async def available_slots(month: int, year: int) -> List[dict]:
    """Find available slots for a given month and year."""
    print(f'FINDING AVAILABLE SLOTS FOR {month}/{year}')
    return [i.prettyprint() for i in await NeetoCalHandler().available_slots(month, year)]

async def book_appointment(name: str, email: str, slot_date: str, slot_start_time: str):
    """Book an appointment."""
    print(f'BOOKING APPOINTMENT FOR {name} EMAIL {email} ON {slot_date} AT {slot_start_time}')
    return await NeetoCalHandler().create_booking(name, email, slot_date, slot_start_time)

TOOL_CALL_MAP = {
    'list_available_slots': available_slots,
    'book_appointment': book_appointment
}
