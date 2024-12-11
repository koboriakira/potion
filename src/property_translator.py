from typing import Any

from src.properties.button import Button
from src.properties.checkbox import Checkbox
from src.properties.created_time import CreatedTime
from src.properties.date import Date
from src.properties.last_edited_time import LastEditedTime
from src.properties.multi_select import MultiSelect
from src.properties.number import Number
from src.properties.properties import Properties
from src.properties.property import Property
from src.properties.relation import Relation
from src.properties.rollup import Rollup
from src.properties.select import Select
from src.properties.status import Status
from src.properties.text import Text
from src.properties.title import Title
from src.properties.url import Url


class PropertyTranslator:
    @classmethod
    def from_dict(cls: "PropertyTranslator", properties: dict[str, dict]) -> Properties:
        values = []
        for key, value in properties.items():
            values.append(cls.from_property_dict(key, value))
        return Properties(values=[value for value in values if value is not None])

    @classmethod
    def from_property_dict(cls: "PropertyTranslator", key: str, property_: dict[str, Any]) -> "Property":  # noqa: PLR0911
        type_ = property_["type"]
        match type_:
            case "title":
                return Title.from_property(key, property_)
            case "rich_text":
                return Text.from_dict(key, property_)
            case "multi_select":
                return MultiSelect.of(key, property_)
            case "select":
                return Select.of(key, property_)
            case "number":
                return Number.of(key, property_)
            case "checkbox":
                return Checkbox.of(key, property_)
            case "date":
                return Date.of(key, property_)
            case "status":
                return Status.of(key, property_)
            case "url":
                return Url.of(key, property_)
            case "relation":
                return Relation.of(key, property_)
            case "last_edited_time":
                return LastEditedTime.create(property_["last_edited_time"])
            case "created_time":
                return CreatedTime.create(property_["created_time"])
            case "rollup":
                return Rollup.of(key, property_)
            case "button":
                return Button.of(key, property_)
            case _:
                msg = f"Unsupported property type: {type_} {property_}"
                raise Exception(msg)