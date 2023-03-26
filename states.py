from aiogram.dispatcher.filters.state import State, StatesGroup

class UpdateMessageText(StatesGroup):
    get_message_text = State() 

class AddLink(StatesGroup):
    get_name = State() 
    get_link = State() 
