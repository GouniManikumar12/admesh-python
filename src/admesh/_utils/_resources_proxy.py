from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `admesh.resources` module.

    This is used so that we can lazily import `admesh.resources` only when
    needed *and* so that users can just import `admesh` and reference `admesh.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("admesh.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
