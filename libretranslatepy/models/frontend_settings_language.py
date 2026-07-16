from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.frontend_settings_language_source import FrontendSettingsLanguageSource
    from ..models.frontend_settings_language_target import FrontendSettingsLanguageTarget


T = TypeVar("T", bound="FrontendSettingsLanguage")


@_attrs_define
class FrontendSettingsLanguage:
    """
    Attributes:
        source (FrontendSettingsLanguageSource | Unset):
        target (FrontendSettingsLanguageTarget | Unset):
    """

    source: FrontendSettingsLanguageSource | Unset = UNSET
    target: FrontendSettingsLanguageTarget | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source: dict[str, Any] | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        target: dict[str, Any] | Unset = UNSET
        if not isinstance(self.target, Unset):
            target = self.target.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_settings_language_source import FrontendSettingsLanguageSource
        from ..models.frontend_settings_language_target import FrontendSettingsLanguageTarget

        d = dict(src_dict)
        _source = d.pop("source", UNSET)
        source: FrontendSettingsLanguageSource | Unset
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = FrontendSettingsLanguageSource.from_dict(_source)

        _target = d.pop("target", UNSET)
        target: FrontendSettingsLanguageTarget | Unset
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = FrontendSettingsLanguageTarget.from_dict(_target)

        frontend_settings_language = cls(
            source=source,
            target=target,
        )

        frontend_settings_language.additional_properties = d
        return frontend_settings_language

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
