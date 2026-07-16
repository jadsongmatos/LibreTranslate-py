from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PostTranslateFileBody")


@_attrs_define
class PostTranslateFileBody:
    """
    Attributes:
        file (File):
        source (str):  Example: en.
        target (str):  Example: es.
        api_key (str | Unset):  Example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.
    """

    file: File
    source: str
    target: str
    api_key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        source = self.source

        target = self.target

        api_key = self.api_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
                "source": source,
                "target": target,
            }
        )
        if api_key is not UNSET:
            field_dict["api_key"] = api_key

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        files.append(("source", (None, str(self.source).encode(), "text/plain")))

        files.append(("target", (None, str(self.target).encode(), "text/plain")))

        if not isinstance(self.api_key, Unset):
            files.append(("api_key", (None, str(self.api_key).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file = File(payload=BytesIO(d.pop("file")))

        source = d.pop("source")

        target = d.pop("target")

        api_key = d.pop("api_key", UNSET)

        post_translate_file_body = cls(
            file=file,
            source=source,
            target=target,
            api_key=api_key,
        )

        post_translate_file_body.additional_properties = d
        return post_translate_file_body

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
