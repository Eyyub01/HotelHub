import openai
from celery import shared_task

from rooms.models.room_models import Room
from hotelhub.settings import OPENAI_API_KEY
from utils.validate_prompts import validate_prompt

openai.api_key = OPENAI_API_KEY

@shared_task
def  ask_ai_for_hotel_detail(room_id, *args, **kwargs):
    try:
        room = Room.objects.filter(id=room_id)
        prompt =(
                f'Tell me about the room {room.type}. '
                f'in {room.hotel.name} located in {room.hotel.location}. '
                f'The room price is {room.price}. '
                f'The room is available {room.is_available}. '
                f'The hotel email is {room.hotel.email}. '
                f'The hotel phone is {room.hotel.phone}. '
                f'The hotel star rating {room.hotel.star_rating}. '
            )
    
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )
    
        ai_response = response.choices[0].text.strip()
        filtered_response = validate_prompt(ai_response)
        return filtered_response
    except Room.DoesNotExist:
        return 'Room not found.'