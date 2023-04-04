from typing import Any, Callable, Dict, List
from objetos.objetos import Objetos

class DisplayFile:
    __displayables: List[Objetos]
    __callbacks: List[Callable[[List[Objetos]], Any]]

    def __init__(self) -> None:
        self.__displayables = []
        self.__callbacks = []

    def __notify_observers(self) -> None:
        for callback in self.__callbacks:
            callback(self.__displayables)

    def __getitem__(self, key: int) -> Objetos:
        return self.__displayables[key]
    
    def subscribe(self, callback: Callable[[List[Objetos]], Any]) -> None:
        self.__callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[List[Objetos]], Any]) -> None:
        self.__callbacks.remove(callback)

    def append(self, displayable: Objetos) -> List[Objetos]:
        self.__displayables.append(displayable)
        self.__notify_observers()
        return self.__displayables
    
    def remove(self, displayable: Objetos) -> List[Objetos]:
        self.__displayables.remove(displayable)
        self.__notify_observers()
        return self.__displayables

    def remove_at(self, index: int) -> List[Objetos]:
        self.__displayables.remove(self.__displayables[index])
        self.__notify_observers()
        return self.__displayables

    def objetos(self) -> List[Objetos]:
        return self.__displayables

    def overwrite(self, new_list: List[Objetos]) -> List[Objetos]:
        self.__displayables = new_list
        self.__notify_observers()
        return self.__displayables