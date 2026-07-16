from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostDetectBody")


@_attrs_define
class PostDetectBody:
    """
    Attributes:
        q (str):  Example: What language is this?.
        api_key (str | Unset):  Example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.
    """

    q: str
    api_key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        q = self.q

        api_key = self.api_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "q": q,
            }
        )
        if api_key is not UNSET:
            field_dict["api_key"] = api_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        q = d.pop("q")

        api_key = d.pop("api_key", UNSET)

        post_detect_body = cls(
            q=q,
            api_key=api_key,
        )

        post_detect_body.additional_properties = d
        return post_detect_body

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
