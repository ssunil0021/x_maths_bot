from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    buttons = [
        [KeyboardButton(text="Today’s Question")],
        [KeyboardButton(text="Past Questions")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)