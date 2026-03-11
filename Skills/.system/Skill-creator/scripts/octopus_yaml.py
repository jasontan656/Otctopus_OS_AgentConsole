"""Compatibility YAML helpers backed by ruamel.yaml."""

from __future__ import annotations

from io import StringIO
from typing import Any, Iterable

from ruamel.yaml import YAML


def _new_yaml(*, allow_unicode: bool = True, sort_keys: bool = False) -> YAML:
    y = YAML(typ="safe")
    y.allow_unicode = allow_unicode
    y.sort_base_mapping_type_on_output = bool(sort_keys)
    return y


def safe_load(stream: Any) -> Any:
    if stream is None:
        return None
    return _new_yaml().load(stream)


def load(stream: Any) -> Any:
    return safe_load(stream)


def safe_load_all(stream: Any) -> Iterable[Any]:
    if stream is None:
        return iter(())
    return _new_yaml().load_all(stream)


def load_all(stream: Any) -> Iterable[Any]:
    return safe_load_all(stream)


def safe_dump(data: Any, stream: Any = None, **kwargs: Any) -> str | None:
    allow_unicode = bool(kwargs.pop("allow_unicode", True))
    sort_keys = bool(kwargs.pop("sort_keys", False))
    y = _new_yaml(allow_unicode=allow_unicode, sort_keys=sort_keys)
    if stream is None:
        buf = StringIO()
        y.dump(data, buf)
        return buf.getvalue()
    y.dump(data, stream)
    return None


def dump(data: Any, stream: Any = None, **kwargs: Any) -> str | None:
    return safe_dump(data, stream=stream, **kwargs)
