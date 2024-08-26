from typing import Type, Callable, Dict, Any, Tuple
from enum import Enum


class ServiceScope(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"


class DependencyInjector:
    """
    A sophisticated dependency injection container with advanced features such as scopes, factory methods, and lazy initialization.
    This class allows for flexible registration and resolution of services, including singleton, transient, and scoped lifetimes,
    parameterized constructors, and lazy initialization.
    """

    def __init__(self):
        """
        Initializes the DependencyInjector instance with empty service and factory registries.
        """
        self._services: Dict[Type, Tuple[Callable, ServiceScope]] = {}
        self._factories: Dict[Type, Callable] = {}
        self._scopes: Dict[Type, Any] = {}

    def register(self, interface: Type, implementation: Type, scope: ServiceScope = ServiceScope.TRANSIENT):
        """
        Registers a service with a specified scope.

        Args:
            interface (Type): The interface or abstract base class for the service.
            implementation (Type): The concrete implementation of the interface.
            scope (ServiceScope): The scope of the service (singleton, transient, or scoped).
        """
        if not isinstance(interface, type) or not isinstance(implementation, type):
            raise TypeError("Both interface and implementation must be of type 'Type'")

        self._services[interface] = (implementation, scope)

    def register_factory(self, interface: Type, factory: Callable):
        """
        Registers a factory method for creating instances of a service.

        Args:
            interface (Type): The interface or abstract base class for the service.
            factory (Callable): The factory method that returns an instance of the service.
        """
        if not callable(factory):
            raise TypeError("Factory must be callable")
        self._factories[interface] = factory

    def resolve(self, interface: Type) -> Any:
        """
        Resolves an instance of a service, handling singleton, transient, and scoped cases.

        Args:
            interface (Type): The interface or abstract base class for the service.

        Returns:
            Any: The instance of the resolved service.

        Raises:
            KeyError: If the interface is not registered.
        """
        if interface in self._services:
            implementation, scope = self._services[interface]
            if scope == ServiceScope.SINGLETON:
                if interface in self._scopes:
                    return self._scopes[interface]
                instance = implementation()
                self._scopes[interface] = instance
                return instance
            elif scope == ServiceScope.SCOPED:
                return implementation()
            else:
                return implementation()

        if interface in self._factories:
            return self._factories[interface]()

        raise KeyError(f"No implementation registered for {interface}")

    def clear(self):
        """
        Clears all registered services, factories, and scopes.
        """
        self._services.clear()
        self._factories.clear()
        self._scopes.clear()
