from babel.support import LazyProxy
from collections.abc import Sequence
from types import MappingProxyType
from typing import Union, Dict

from aiogram.types import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup

from safe_pass.keyboards.utils import create_keyboard_layout

class ReplyConstructor:

    aliases = MappingProxyType({
        "contact": "request_contact",
        "location": "request_location",
        "poll": "request_poll",
    })
    available_properties = (
        "text",
        "request_contact",
        "request_location",
        "request_poll",
        "request_user",
        "request_chat",
        "web_app",
    )
    properties_amount = 1

    @staticmethod
    def _create_kb(
        actions: Sequence[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]],
        schema: Sequence[int],
        resize_keyboard: bool = True,
        selective: bool = False,
        one_time_keyboard: bool = False,
        is_persistent: bool = True,
    ) -> ReplyKeyboardMarkup:
        btns: list[KeyboardButton] = []
        
        for a in actions:
            if isinstance(a, str):
                a = {"text": a}
            data: Dict[str, Union[str, bool, KeyboardButtonPollType]] = {}
            for k, v in ReplyConstructor.aliases.items():
                if k in a:
                    a[v] = a[k]
                    del a[k]
            for k in a:
                if k in ReplyConstructor.available_properties:
                    if len(data) < ReplyConstructor.properties_amount:
                        data[k] = a[k]
                    else:
                        break
            if len(data) != ReplyConstructor.properties_amount:
                raise ValueError("Insufficient data to create a button")
            if isinstance(data['text'], LazyProxy):
                data['text'] = data['text'].value
            btns.append(KeyboardButton(**data))
        
        kb = ReplyKeyboardMarkup(
            resize_keyboard=resize_keyboard,
            selective=selective,
            one_time_keyboard=one_time_keyboard,
            is_persistent=is_persistent,
            keyboard=create_keyboard_layout(btns, schema),
        )
        return kb
