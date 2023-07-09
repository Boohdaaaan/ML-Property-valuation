import joblib
import pandas as pd

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards import *
from states import *
from text_blanks import ABOUT


model = joblib.load('models/xgb_v1.joblib')


async def exit(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ви повернулися до головного меню', reply_markup=get_main_kb())


async def start_cmd(message: types.Message):
    await message.answer('Ласкаво просимо! \nЗа допомогою цього бота ви можете дізнатися орієнтовну вартість квартир'
                         'вторинного ринку України.', parse_mode='HTML', reply_markup=get_main_kb())


async def site_link(message: types.Message):
    await message.answer('http://ec2-18-193-85-100.eu-central-1.compute.amazonaws.com:5000/')


async def about_project(message: types.Message):
    await message.answer(ABOUT, parse_mode='HTML')


async def enter_data(message: types.Message):
    await message.answer('Напишіть місто', reply_markup=get_exit_kb())
    await AllStatesGroup.City.set()


async def select_city(message: types.Message, state: FSMContext):
    data = pd.read_csv('data/data_cities.csv')
    mess = message.text.capitalize()
    if mess in data['Location'].to_list():
        reg = data[data.Location == mess]['Region'].iloc[0]
        city = data[data.Location == mess]['City'].iloc[0]
        async with state.proxy() as data:
            data['region'] = reg
            data['city'] = city
        await message.answer('Напишіть площу квартири')
        await AllStatesGroup.next()
    else:
        await message.answer('Такого міста не знайдено')


async def save_area(message: types.Message, state: FSMContext):
    try:
        if float(message.text) > 500.0:
            await message.answer('Занадто велика площа')
        elif float(message.text) < 10.0:
            await message.answer('Занадто мала площа')
        else:
            async with state.proxy() as data:
                data['area'] = float(message.text)
            await message.answer('Вкажіть кількість кімнат', reply_markup=ikb_rooms())
            await AllStatesGroup.next()
    except:
        await message.answer('Невірний тип даних')


async def save_rooms(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['rooms'] = callback.data
    await callback.answer('Дякую!')
    await callback.bot.edit_message_text(text='Тепер вкажіть поверх', reply_markup=ikb_floor(),
                                         message_id=callback.message.message_id, chat_id=callback.from_user.id)
    await AllStatesGroup.next()


async def save_floor(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Дякую!')
    async with state.proxy() as data:
        data['floor'] = callback.data

    data = {'Region': data['region'], 'City': data['city'], 'Floor': data['floor'], 'Area': data['area'], 'Rooms': data['rooms']}
    df = pd.DataFrame(data=data, index=['1'])
    predicted_value = round(model.predict(df)[0])
    full_price = '{0:,}'.format(int(predicted_value * df['Area'][0])).replace(',', ' ')
    predicted_value = '{0:,}'.format(predicted_value).replace(',', ' ')

    predict_text = f"""
    *Орієнтовна ціна з такими параметрами 💰*\n\n_Ціна за об'єкт - ${full_price}\nЦіна за м² - ${predicted_value}_
    """

    await callback.bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)
    await callback.bot.send_message(text=predict_text, chat_id=callback.from_user.id, parse_mode='Markdown',
                                    reply_markup=get_main_kb())
    await state.finish()


def register_handler_user(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'], state=None)
    dp.register_message_handler(exit, Text(equals='Назад 🔙'), state='*')
    dp.register_message_handler(site_link, Text(equals='Перейти на сайт'), state=None)
    dp.register_message_handler(about_project, Text(equals='Про проєкт'), state=None)
    dp.register_message_handler(enter_data, Text(equals='Прорахувати ціну'), state=None)
    dp.register_message_handler(select_city, state=AllStatesGroup.City)
    dp.register_message_handler(save_area, state=AllStatesGroup.Area)
    dp.register_callback_query_handler(save_rooms, state=AllStatesGroup.Rooms)
    dp.register_callback_query_handler(save_floor, state=AllStatesGroup.Floor)
