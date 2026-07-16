from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.frontend_settings_language import FrontendSettingsLanguage


T = TypeVar("T", bound="FrontendSettings")


@_attrs_define
class FrontendSettings:
    """
    Attributes:
        api_keys (bool | Unset): Whether the API key database is enabled.
        char_limit (int | Unset): Character input limit for this language (-1 indicates no limit)
        frontend_timeout (int | Unset): Frontend translation timeout
        key_required (bool | Unset): Whether an API key is required.
        language (FrontendSettingsLanguage | Unset):
        suggestions (bool | Unset): Whether submitting suggestions is enabled.
        supported_files_format (list[str] | Unset): Supported files format
    """

    api_keys: bool | Unset = UNSET
    char_limit: int | Unset = UNSET
    frontend_timeout: int | Unset = UNSET
    key_required: bool | Unset = UNSET
    language: FrontendSettingsLanguage | Unset = UNSET
    suggestions: bool | Unset = UNSET
    supported_files_format: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_keys = self.api_keys

        char_limit = self.char_limit

        frontend_timeout = self.frontend_timeout

        key_required = self.key_required

        language: dict[str, Any] | Unset = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.to_dict()

        suggestions = self.suggestions

        supported_files_format: list[str] | Unset = UNSET
        if not isinstance(self.supported_files_format, Unset):
            supported_files_format = self.supported_files_format

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api_keys is not UNSET:
            field_dict["apiKeys"] = api_keys
        if char_limit is not UNSET:
            field_dict["charLimit"] = char_limit
        if frontend_timeout is not UNSET:
            field_dict["frontendTimeout"] = frontend_timeout
        if key_required is not UNSET:
            field_dict["keyRequired"] = key_required
        if language is not UNSET:
            field_dict["language"] = language
        if suggestions is not UNSET:
            field_dict["suggestions"] = suggestions
        if supported_files_format is not UNSET:
            field_dict["supportedFilesFormat"] = supported_files_format

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_settings_language import FrontendSettingsLanguage

        d = dict(src_dict)
        api_keys = d.pop("apiKeys", UNSET)

        char_limit = d.pop("charLimit", UNSET)

        frontend_timeout = d.pop("frontendTimeout", UNSET)

        key_required = d.pop("keyRequired", UNSET)

        _language = d.pop("language", UNSET)
        language: FrontendSettingsLanguage | Unset
        if isinstance(_language, Unset):
            language = UNSET
        else:
            language = FrontendSettingsLanguage.from_dict(_language)

        suggestions = d.pop("suggestions", UNSET)

        supported_files_format = cast(list[str], d.pop("supportedFilesFormat", UNSET))

        frontend_settings = cls(
            api_keys=api_keys,
            char_limit=char_limit,
            frontend_timeout=frontend_timeout,
            key_required=key_required,
            language=language,
            suggestions=suggestions,
            supported_files_format=supported_files_format,
        )

        frontend_settings.additional_properties = d
        return frontend_settings

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
