"""Contains all the data models used in inputs/outputs"""

from .detections_item import DetectionsItem
from .error_response import ErrorResponse
from .error_slow_down import ErrorSlowDown
from .frontend_settings import FrontendSettings
from .frontend_settings_language import FrontendSettingsLanguage
from .frontend_settings_language_source import FrontendSettingsLanguageSource
from .frontend_settings_language_target import FrontendSettingsLanguageTarget
from .health_response import HealthResponse
from .languages_item import LanguagesItem
from .post_detect_body import PostDetectBody
from .post_suggest_body import PostSuggestBody
from .post_translate_body import PostTranslateBody
from .post_translate_body_format import PostTranslateBodyFormat
from .post_translate_file_body import PostTranslateFileBody
from .suggest_response import SuggestResponse
from .translate import Translate
from .translate_detected_language import TranslateDetectedLanguage
from .translate_file import TranslateFile

__all__ = (
    "DetectionsItem",
    "ErrorResponse",
    "ErrorSlowDown",
    "FrontendSettings",
    "FrontendSettingsLanguage",
    "FrontendSettingsLanguageSource",
    "FrontendSettingsLanguageTarget",
    "HealthResponse",
    "LanguagesItem",
    "PostDetectBody",
    "PostSuggestBody",
    "PostTranslateBody",
    "PostTranslateBodyFormat",
    "PostTranslateFileBody",
    "SuggestResponse",
    "Translate",
    "TranslateDetectedLanguage",
    "TranslateFile",
)
