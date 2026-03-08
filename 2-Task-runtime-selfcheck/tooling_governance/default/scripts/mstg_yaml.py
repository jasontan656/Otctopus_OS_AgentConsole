from __future__ import annotations

from io import StringIO
from typing import Any

from ruamel.yaml import YAML


def _yaml_safe() -> YAML:
    return YAML(typ="safe")


def _yaml_rt(*, allow_unicode: bool = True) -> YAML:
    y = YAML(typ="rt")
    y.preserve_quotes = True
    y.indent(mapping=2, sequence=4, offset=2)
    y.width = 120
    y.allow_unicode = allow_unicode
    return y


def _sort_obj(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {key: _sort_obj(obj[key]) for key in sorted(obj)}
    if isinstance(obj, list):
        return [_sort_obj(item) for item in obj]
    return obj


def safe_load(text: str) -> Any:
    if text is None:
        return None
    return _yaml_safe().load(text)


def safe_load_all(text: str):
    return _yaml_safe().load_all(text)


def safe_dump(
    data: Any,
    *,
    allow_unicode: bool = True,
    sort_keys: bool = False,
    **_: Any,
) -> str:
    payload = _sort_obj(data) if sort_keys else data
    buf = StringIO()
    _yaml_rt(allow_unicode=allow_unicode).dump(payload, buf)
    text = buf.getvalue()
    if not text.endswith("\n"):
        text += "\n"
    return text
