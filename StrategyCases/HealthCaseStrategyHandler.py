from typing import Tuple
from StrategyCases.IStrategyHealthCase import IStrategyHealthCase


class HealthCaseStrategyHandler:
    def __init__(self,strategyHealth:IStrategyHealthCase):
        self.strategyHealth = strategyHealth

    def GetResultsCase(self) -> Tuple[int, int]:
        return self.strategyHealth.Run()

    def GetPercentage(self) -> str:
        return self.strategyHealth.CalculatePercentage()

    def GetCaseName(self) -> str:
        return self.strategyHealth.GetCaseName()

    def GetTTestResult(self) -> str:
        return self.strategyHealth.TTestCalculator()

    def GetLinearRegressionResult(self) -> str:
        return self.strategyHealth.LinearRegression()

    def GetAnovaTestResult(self, groupByColumn: str, beforeOrAfter: str) -> str:
        return self.strategyHealth.AnovaTestBy(groupByColumn, beforeOrAfter)