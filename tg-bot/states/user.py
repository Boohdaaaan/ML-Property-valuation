from aiogram.dispatcher.filters.state import StatesGroup, State


class AllStatesGroup(StatesGroup):
    City = State()
    Area = State()
    Rooms = State()
    Floor = State()


