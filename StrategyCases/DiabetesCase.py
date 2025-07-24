from typing import Tuple
from Helpers.DataPreprocessor import DataPreprocessor
from Helpers.ResultAnalyzer import ResultAnalyzer
from Helpers.ValueParser import ValueParser
from StrategyCases.IStrategyHealthCase import IStrategyHealthCase


class DiabetesCase(IStrategyHealthCase):
    def __init__(self):
        self.result:Tuple[int, int] = (0, 0) # To save the positive and negative values
        self.CaseName = "Diabetes"
        self.requiredFields = ["HbA1c_Before", "HbA1c_After"]

    #This private method responsible to return the HbA1c values(Before and After)
    def _GetRequestedColumnValues(self, userRequestedField: str, conditionFilter: dict[str, str])-> list[float]:

        rows = DataPreprocessor.LoadCaseByConditionFromExcel(column=conditionFilter["Column"],
                                                             value=conditionFilter["Value"],
                                                             requiredFields=self.requiredFields)

        values = []
        for row in rows:
            value = row.get(f"HbA1c_{userRequestedField}")
            if value is None or str(value).strip() == "":
                continue
            try:
                values.append(ValueParser.StripRemover(value))
            except:
                continue

        return values

    #This private method responsible to group a given column name with a given row values
    def _GroupRowsByColumnValueNew(self, groupByColumn:str, valueField:str, conditionFilter:dict[str, str])-> dict[str, list[float]]:
        rows = DataPreprocessor.LoadCaseByConditionFromExcel(column=conditionFilter["Column"],
                                                             value=conditionFilter["Value"],
                                                             requiredFields=self.requiredFields + [groupByColumn])

        grouped = dict()
        for row in rows:
            groupKey = row.get(groupByColumn)
            value = row.get(valueField)

            if not groupKey or value is None or str(value).strip() == "":
                continue

            try:
                parsedValue = ValueParser.StripRemover(value)
            except:
                continue

            if groupKey not in grouped:
                grouped[groupKey] = []
            grouped[groupKey].append(parsedValue)

        return grouped

    #This is method responsible to return the positive and negative cases
    def Run(self) -> Tuple[int, int]:
        old_Values = self._GetRequestedColumnValues("Before", {"Column": "Condition", "Value": self.CaseName})
        new_Values = self._GetRequestedColumnValues("After", {"Column": "Condition", "Value": self.CaseName})

        positiveCounts = 0
        negativeCounts = 0

        for oldResult,newResult in zip(old_Values, new_Values):
            if oldResult > newResult:
                positiveCounts += 1
            else:
                negativeCounts += 1

        self.result = (positiveCounts, negativeCounts)
        return self.result

    def GetCaseName(self) -> str:
        return self.CaseName

    def CalculatePercentage(self) -> str:
        return f"The diabetes improvement is {ResultAnalyzer.CalculatePercentageBase(self.result):.2f}%"

    def TTestCalculator(self) -> str:
        oldValues = self._GetRequestedColumnValues("Before", {"Column": "Condition", "Value": self.CaseName})
        newValues = self._GetRequestedColumnValues("After", {"Column": "Condition", "Value": self.CaseName})

        tTestResult = ResultAnalyzer.TTestCalculatorBase(oldValues, newValues, self.CaseName)

        return tTestResult

    def LinearRegression(self) -> str:
        beforeValues = self._GetRequestedColumnValues("Before", {"Column": "Condition", "Value": self.CaseName})
        afterValues = self._GetRequestedColumnValues("After", {"Column": "Condition", "Value": self.CaseName})

        return ResultAnalyzer.LinearRegressionBase(beforeValues, afterValues, self.CaseName)

    def AnovaTestBy(self, groupByColumn: str, beforeOrAfter: str) -> str:
        valueColumn = f"HbA1c_{beforeOrAfter}"
        grouped = self._GroupRowsByColumnValueNew(groupByColumn, valueColumn,
                                                 conditionFilter={"Column": "Condition", "Value": self.CaseName})

        return ResultAnalyzer.AnovaTestBase(*grouped.values())