from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_translate_body_format import PostTranslateBodyFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostTranslateBody")


@_attrs_define
class PostTranslateBody:
    """
    Attributes:
        q (str):
        source (str):  Example: en.
        target (str):  Example: es.
        format_ (PostTranslateBodyFormat | Unset):  Default: PostTranslateBodyFormat.TEXT. Example: text.
        alternatives (int | Unset):  Default: 0. Example: 3.
        api_key (str | Unset):  Example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.
    """

    q: str
    source: str
    target: str
    format_: PostTranslateBodyFormat | Unset = PostTranslateBodyFormat.TEXT
    alternatives: int | Unset = 0
    api_key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        q = self.q

        source = self.source

        target = self.target

        format_: str | Unset = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value

        alternatives = self.alternatives

        api_key = self.api_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "q": q,
                "source": source,
                "target": target,
            }
        )
        if format_ is not UNSET:
            field_dict["format"] = format_
        if alternatives is not UNSET:
            field_dict["alternatives"] = alternatives
        if api_key is not UNSET:
            field_dict["api_key"] = api_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        q = d.pop("q")

        source = d.pop("source")

        target = d.pop("target")

        _format_ = d.pop("format", UNSET)
        format_: PostTranslateBodyFormat | Unset
        if isinstance(_format_, Unset):
            format_ = UNSET
        else:
            format_ = PostTranslateBodyFormat(_format_)

        alternatives = d.pop("alternatives", UNSET)

        api_key = d.pop("api_key", UNSET)

        post_translate_body = cls(
            q=q,
            source=source,
            target=target,
            format_=format_,
            alternatives=alternatives,
            api_key=api_key,
        )

        post_translate_body.additional_properties = d
        return post_translate_body

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
