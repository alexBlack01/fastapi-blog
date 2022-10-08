from typing import Any, Callable, Optional

import orjson


def orjson_dumps(v: Any, *, default: Optional[Callable[[Any], Any]]):  # noqa: WPS111
    """Helper to decode orsjon result (bytes) as str.

    :param v:
        value to decode
    :param default:
        default param for orjson dumps
    :return: str
        Returns json string
    """
    orjson_option = orjson.OPT_NAIVE_UTC | orjson.OPT_NON_STR_KEYS
    return orjson.dumps(v, default=default, option=orjson_option).decode()
