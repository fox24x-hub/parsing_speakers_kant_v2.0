from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def topics_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="ЗИМА 🏔", callback_data="season:зима")
    builder.button(text="ЛЕТО ☀️", callback_data="season:лето")
    builder.button(text="Екатеринбург", callback_data="region:екатеринбург")
    builder.button(text="УрФО", callback_data="region:урфо")
    builder.button(text="Россия", callback_data="region:россия")
    builder.adjust(2, 3)
    return builder.as_markup()
