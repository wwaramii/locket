from types import MappingProxyType
from typing import TypeVar, Union, List, Dict

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    CallbackGame,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LoginUrl,
)

from safe_pass.keyboards.utils import create_keyboard_layout

A = TypeVar("A", bound=CallbackData)

class InlineConstructor:
    aliases = MappingProxyType({"cb": "callback_data"})
    available_properties = (
        "text",
        "callback_data",
        "url",
        "login_url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
        "pay",
    )
    properties_amount = 2

    @staticmethod
    def _create_kb(
        actions: List[Dict[str, Union[str, bool, A, LoginUrl, CallbackGame]]],
        schema: List[int],
    ) -> InlineKeyboardMarkup:
        btns: List[InlineKeyboardButton] = []
        
        for a in actions:
            data: Dict[str, Union[str, bool, A, LoginUrl, CallbackGame]] = {}
            for k, v in InlineConstructor.aliases.items():
                if k in a:
                    a[v] = a[k]
                    del a[k]
            for k in a:
                if k in InlineConstructor.available_properties:
                    if len(data) < InlineConstructor.properties_amount:
                        data[k] = a[k]
                    else:
                        break
            if "callback_data" in data and isinstance(data["callback_data"], CallbackData):
                data["callback_data"] = data["callback_data"].pack()
            if "pay" in data:
                if btns and data["pay"]:
                    raise ValueError("The payment button must be the first in the keyboard")
                data["pay"] = a["pay"]
            if len(data) != InlineConstructor.properties_amount:
                raise ValueError("Insufficient data to create a button")
            btns.append(InlineKeyboardButton(**data))
        
        kb = InlineKeyboardMarkup(inline_keyboard=create_keyboard_layout(btns, schema))
        return kb
