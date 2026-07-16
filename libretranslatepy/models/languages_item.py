from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LanguagesItem")


@_attrs_define
class LanguagesItem:
    """Supported language

    Attributes:
        code (str | Unset): Language code
        name (str | Unset): Human-readable language name (in English)
        targets (list[str] | Unset): Supported target language codes
    """

    code: str | Unset = UNSET
    name: str | Unset = UNSET
    targets: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        name = self.name

        targets: list[str] | Unset = UNSET
        if not isinstance(self.targets, Unset):
            targets = self.targets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if name is not UNSET:
            field_dict["name"] = name
        if targets is not UNSET:
            field_dict["targets"] = targets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code", UNSET)

        name = d.pop("name", UNSET)

        targets = cast(list[str], d.pop("targets", UNSET))

        languages_item = cls(
            code=code,
            name=name,
            targets=targets,
        )

        languages_item.additional_properties = d
        return languages_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
