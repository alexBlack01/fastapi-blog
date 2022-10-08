from enum import Enum
from typing import Any, Callable, Optional, Type, TypeVar

import punq

_container = punq.Container()

GenericType = TypeVar('GenericType')  # Can be anything


class Scope(Enum):
    transient = 0
    singleton = 1


def register(
        service: Type,
        factory: Optional[Callable] = None,
        instance: Optional[Any] = None,
        scope: Scope = Scope.transient,
        **kwargs,
) -> None:
    """Register new type in IoC-container and what that type resolves to.

    :param service:
        Type to register, if no other arguments passed function can be used as decorator
    :param factory:
        Factory callable to return object which implements type signature
    :param instance:
        Single instance to implement Type
    :param scope:
        Singleton objects or create-by-demand
    """
    _container.register(
        service=service, factory=factory, instance=instance, scope=scope, **kwargs,
    )


def resolve(service: Type[GenericType], **kwargs) -> GenericType:
    """Return Type implementation.

    :param service:
        needed Type
    :param kwargs:
    :return: T
        Object of requested Type
    """
    return _container.resolve(service_key=service, **kwargs)
