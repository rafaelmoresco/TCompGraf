from typing import Any, Callable, Dict, List
from model.displayable import Displayable


# A "observable" that holds displayables
class ObservableDisplayFile:
    ### Private attrs
    __displayables: List[Displayable]
    __callbacks: List[Callable[[List[Displayable]], Any]]

    # Constructor
    def __init__(self) -> None:
        self.__displayables = []
        self.__callbacks = []

    ### Private methods
    def __notify_observers(self) -> None:
        for callback in self.__callbacks:
            callback(self.__displayables)

    ### Public methods
    def subscribe(self, callback: Callable[[List[Displayable]], Any]) -> None:
        self.__callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[List[Displayable]], Any]) -> None:
        self.__callbacks.remove(callback)

    def append(self, displayable: Displayable) -> List[Displayable]:
        self.__displayables.append(displayable)
        self.__notify_observers()
        return self.__displayables
    
    def remove(self, displayable: Displayable) -> List[Displayable]:
        self.__displayables.remove(displayable)
        self.__notify_observers()
        return self.__displayables

    def remove_at(self, index: int) -> List[Displayable]:
        self.__displayables.remove(self.__displayables[index])
        self.__notify_observers()
        return self.__displayables

    def displayables(self) -> List[Displayable]:
        return self.__displayables