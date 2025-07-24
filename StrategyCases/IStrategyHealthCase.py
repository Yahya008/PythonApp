from abc import ABC, abstractmethod
from typing import Tuple

#abc:Abstract base class
#It’s a built-in Python module used to define abstract classes and interfaces.

class IStrategyHealthCase(ABC): # This is like an interface
    @abstractmethod
    def GetCaseName(self) -> str:
        pass

    @abstractmethod
    def Run(self)-> Tuple[int, int]:
        pass

    @abstractmethod
    def CalculatePercentage(self) -> str:
        pass

    @abstractmethod
    def TTestCalculator(self) -> str:
        pass

    @abstractmethod
    def LinearRegression(self) -> str:
        pass

    @abstractmethod
    def AnovaTestBy(self,group_by_column: str, value_column: str) -> str:
        pass

#Any class like DiabetesCase or HyperTensionCase that extends IStrategyCase must define all these functions: