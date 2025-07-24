from typing import Tuple
from Helpers.DataPreprocessor import DataPreprocessor
from Helpers.ResultAnalyzer import ResultAnalyzer
from Helpers.ValueParser import ValueParser
from StrategyCases.IStrategyHealthCase import IStrategyHealthCase


class HyperTensionCase(IStrategyHealthCase):
    def __init__(self):
        self.result:Tuple[int, int] = (0, 0) # To save the positive and negative values
        self.CaseName = "Hypertension"
        self.requiredFields = ["BP_Before", "BP_After"] # requestedField for the systolic or diastolic

    # Private Method for the class
    def _GetRequestedColumnValues(self,userRequestedField: str, conditionFilter: dict[str, str]) -> list[float]:

        rows = DataPreprocessor.LoadCaseByConditionFromExcel(column=conditionFilter["Column"],
                                                             value=conditionFilter["Value"],
                                                             requiredFields=self.requiredFields)

        values = []
        for row in rows:
            value = row.get(f"BP_{userRequestedField}")
            if value is None or str(value).strip() == "":
                continue
            try:
                values.append(list(ValueParser.ParseBloodPressure(value)))  # returns (systolic, diastolic)
            except:
                continue

        return values #[[160, 100], [146, 96], [144, 91], [153, 90]]

    def _GroupBpByColumn(self, groupByColumn:str, valueField:str, conditionFilter:dict[str, str]) -> dict[str, list[float]]:

        rows = DataPreprocessor.LoadCaseByConditionFromExcel(column=conditionFilter["Column"],
                                                             value=conditionFilter["Value"],
                                                             requiredFields=self.requiredFields)

        grouped = dict()

        for row in rows:
            groupKey = row.get(groupByColumn)
            value = row.get(valueField)

            if not groupKey or value is None or str(value).strip() == "":
                continue

            try:
                parsedBpValue = ValueParser.ParseBloodPressure(value)
            except:
                continue

            # Initialize list if key doesn't exist, then ALWAYS append
            if groupKey not in grouped:
                grouped[groupKey] = []
            grouped[groupKey].append(tuple(parsedBpValue)) # Now appends all valid values

        return grouped

    # Private Method for the class
    def _GetSplitSystolicAndDiastolic(self) -> Tuple[list[float], list[float], list[float], list[float]]:
        # Get all before/after blood pressure readings
        old_Values = self._GetRequestedColumnValues("Before",{"Column": "Condition", "Value": self.CaseName})
        new_Values = self._GetRequestedColumnValues("After",{"Column": "Condition", "Value": self.CaseName})

        # Helper lambda to split systolic/diastolic values from tuples
        splitBpValues = lambda values: ([sys for sys, _ in values], [dias for _, dias in values])

        old_Systolic, old_Diastolic = splitBpValues(old_Values)
        new_Systolic, new_Diastolic = splitBpValues(new_Values)

        return old_Systolic, new_Systolic, old_Diastolic, new_Diastolic

    def Run(self) -> Tuple[int, int]:
        old_Systolic,new_Systolic,old_Diastolic,new_Diastolic = self._GetSplitSystolicAndDiastolic()

        positiveCounts = 0
        negativeCounts = 0

        for i in range(len(old_Systolic)):
            if new_Systolic[i] < old_Systolic[i] and new_Diastolic[i] < old_Diastolic[i]:
                positiveCounts += 1
            else:
                negativeCounts += 1

        self.result = (positiveCounts, negativeCounts)

        return self.result

    def GetCaseName(self) -> str:
        return self.CaseName

    def CalculatePercentage(self) -> str:
        return f"The hypertension improvement is {ResultAnalyzer.CalculatePercentageBase(self.result):.2f}%"

    def TTestCalculator(self) -> str:
        (oldSystolicValues,newSystolicValues,
         oldDiastolicValues,newDiastolicValues) = self._GetSplitSystolicAndDiastolic()

        sysTTestResult = ResultAnalyzer.TTestCalculatorBase(oldSystolicValues, newSystolicValues,
                                                            self.CaseName + " Systolic")
        diasTTestResult = ResultAnalyzer.TTestCalculatorBase(oldDiastolicValues, newDiastolicValues,
                                                             self.CaseName + " Diastolic")

        finalTTestResult = f"{sysTTestResult}\n\n{diasTTestResult}"

        return finalTTestResult

    def LinearRegression(self) -> str:
        old_Systolic, new_Systolic, old_Diastolic, new_Diastolic = self._GetSplitSystolicAndDiastolic()

        systolicResult = ResultAnalyzer.LinearRegressionBase(old_Systolic, new_Systolic, self.CaseName)
        diastolicResult = ResultAnalyzer.LinearRegressionBase(old_Diastolic, new_Diastolic,self.CaseName)

        return systolicResult + "\n\n" + diastolicResult

    def AnovaTestBy(self, group_by_column: str, value_column: str) -> str:
        grouped = self._GroupBpByColumn(group_by_column, value_column, {
            "Column": "Condition", "Value": self.CaseName
        })

        if value_column.endswith("Before"):
            index = 0
        else:
            index = 1

        # Extract systolic or diastolic values only
        groupedCleaned = {
            k:[bp[index] for bp in v] for k, v in grouped.items()
        }

        return ResultAnalyzer.AnovaTestBase(*groupedCleaned.values())