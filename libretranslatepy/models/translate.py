from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.translate_detected_language import TranslateDetectedLanguage


T = TypeVar("T", bound="Translate")


@_attrs_define
class Translate:
    """
    Attributes:
        translated_text (str):
        alternatives (str | Unset):
        detected_language (TranslateDetectedLanguage | Unset):
    """

    translated_text: str
    alternatives: str | Unset = UNSET
    detected_language: TranslateDetectedLanguage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        translated_text = self.translated_text

        alternatives = self.alternatives

        detected_language: dict[str, Any] | Unset = UNSET
        if not isinstance(self.detected_language, Unset):
            detected_language = self.detected_language.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "translatedText": translated_text,
            }
        )
        if alternatives is not UNSET:
            field_dict["alternatives"] = alternatives
        if detected_language is not UNSET:
            field_dict["detectedLanguage"] = detected_language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.translate_detected_language import TranslateDetectedLanguage

        d = dict(src_dict)
        translated_text = d.pop("translatedText")

        alternatives = d.pop("alternatives", UNSET)

        _detected_language = d.pop("detectedLanguage", UNSET)
        detected_language: TranslateDetectedLanguage | Unset
        if isinstance(_detected_language, Unset):
            detected_language = UNSET
        else:
            detected_language = TranslateDetectedLanguage.from_dict(_detected_language)

        translate = cls(
            translated_text=translated_text,
            alternatives=alternatives,
            detected_language=detected_language,
        )

        translate.additional_properties = d
        return translate

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
