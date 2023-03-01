from aiogram import Bot, Dispatcher, types, executor

import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Translator.googletranslate import translator

token = '5917805579:AAGwbAasszLw9CJbQE1HBFG_cLd8S36aTIQ'

bot = Bot(token)

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

inline_buttons = [
    [('q', 'q'), ('w', 'w'), ('e', 'e'), ('r', 'r'), ('t', 't'), ('y', 'y'), ('u', 'u'), ('i', 'i')],
    [('o', 'o'), ('p', 'p'), ('a', 'a'), ('s', 's'), ('d', 'd'), ('f', 'f'), ('g', 'g'), ('h', 'h')],
    [('j', 'j'), ('k', 'k'), ('l', 'l'), ('z', 'z'), ('x', 'x'), ('c', 'c'), ('v', 'v'), ('b', 'b')],
    [('n', 'n'), ('m', 'm'), ('.', '.'), ("'", "'"), ('🧹', '🧹'), ('⬅', '⬅')],
    [('✅', '✅')]
]


def buttons():
    ikm = InlineKeyboardMarkup(row_width=9)
    for button in inline_buttons:
        ikm.add(*[InlineKeyboardButton(data, callback_data=call_back) for data, call_back in button])
    return ikm


@dp.message_handler(commands='start')
async def start(message: types.Message):
    ikm = buttons()
    await message.answer('Translator : ', reply_markup=ikm)


@dp.callback_query_handler()
async def query(call_back: types.CallbackQuery):
    ikm = buttons()
    text = call_back.message.text.split('Translator :')[-1]
    if call_back.data.isalnum() or call_back.data in ".'":
        text = call_back.message.text + call_back.data
    if call_back.data == '🧹':
        text = f"Translator :"

    if call_back.data == '⬅':
        if not len(text):
            return
        text = f"Translator :{text[0:-1]}"
    if call_back.data == '✅':
        lang = translator.detect(text).lang
        dest = 'uz' if lang == 'en' else 'en'
        await bot.answer_callback_query(callback_query_id=call_back.id,
                                        text=translator.translate(call_back.message.text[12:], dest).text,
                                        show_alert=True)
        text = f"Translator :"
    await bot.edit_message_text(text=text, chat_id=call_back.message.chat.id, message_id=call_back.message.message_id
                                , reply_markup=ikm)


executor.start_polling(dp, skip_updates=True)