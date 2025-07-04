from typing import Tuple
from StrategyCases.IStrategyHealthCase import IStrategyHealthCase


class HealthCaseStrategyHandler:
    def __init__(self,strategyHealth:IStrategyHealthCase):
        self.strategyHealth = strategyHealth

    def GetResultsCase(self) -> Tuple[int, int]:
        healthCases = self.strategyHealth.Run()
        return healthCases

    def GetPercentage(self) -> str:
        return self.strategyHealth.CalculatePercentage()

    def GetCaseName(self) -> str:
        return self.strategyHealth.GetCaseName()

    def GetTTestResult(self) -> str:
        return self.strategyHealth.TTestCalculator()

    def GetLinearRegressionResult(self) -> str:
        return self.strategyHealth.LinearRegression()
