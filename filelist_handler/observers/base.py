"""Base observer pattern classes"""

from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """Abstract observer for event notifications"""
    
    @abstractmethod
    def update(self, event: str, data: dict):
        """Handle event notification"""
        pass


class Subject:
    """Subject that notifies observers"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: str, data: dict):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(event, data)

