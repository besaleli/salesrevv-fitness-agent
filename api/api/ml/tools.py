"""Tools."""
from typing import List
from sqlalchemy import select
from .embedding import embedding
from ..integrations.neetocal import NeetoCalHandler
from ..models.document import Document
from ..db import SessionLocal

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

SEARCH_FITNESS_INFORMATION = {
    'type': 'function',
    'function': {
        'name': 'search_fitness_information',
        'description': 'Search for information about fitness given a natural language query. Augment your response from the user with these search results.',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'Search query. Example: "Health benefits of fitness'
                },
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

async def vector_search(query: str) -> str:
    """Vector search."""
    query_embedding = await embedding([query])
    query_embedding = query_embedding[0]

    with SessionLocal() as session:
        documents : List[tuple[Document]] = session.execute(
            select(Document)
            .order_by(Document.embedding.l2_distance(query_embedding))
            .limit(3)
            ).all()

    return '\n\n'.join(i[0].content for i in documents)

TOOL_CALL_MAP = {
    'list_available_slots': available_slots,
    'book_appointment': book_appointment,
    'search_fitness_information': vector_search
}
