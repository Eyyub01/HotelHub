import openai
from celery import shared_task

from ai.models import AiResponse
from rooms.models.room_models import Room
from hotelhub.settings import OPENAI_API_KEY
from utils.validate_prompts import validate_prompt

openai.api_key = OPENAI_API_KEY

@shared_task
def  ai_for_hotel_and_room(room_id, *args, **kwargs):
    try:
        room = Room.objects.get(id=room_id)
        prompt =(
                f'Tell me about the room {room.type}. '
                f'in {room.hotel.name} located in {room.hotel.address}. '
                f'The room price is {room.price}. '
                f'The room is available {room.is_available}. '
                f'The hotel email is {room.hotel.email}. '
                f'The hotel phone is {room.hotel.phone}. '
                f'The hotel star rating {room.hotel.star_rating}. '
            )
    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens= 200, 
            temperature=0.7
        )
        
        ai_response = response.choices[0].text.strip()
        filtered_response = validate_prompt(ai_response)

        ai_response_instance = AiResponse.objects.create(
            room_id=room_id,
            ai_response=filtered_response,
            processed=True  
        )

        return filtered_response
    except Room.DoesNotExist:
        return 'Room not found.'