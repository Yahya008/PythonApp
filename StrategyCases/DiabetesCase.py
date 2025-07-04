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
        self.diabetesRows = DataPreprocessor.LoadCaseByConditionFromExcel("Condition", self.CaseName, self.requiredFields)

    #This is a private method no one can call this function
    def _GetRequestedFields(self, userRequestedField : str) -> list[float]:
        values = []

        for diabeteRow in self.diabetesRows:
            diabetesValues = ValueParser.StripRemover(diabeteRow[f"HbA1c_{userRequestedField}"])
            values.append(diabetesValues)
            #[8.9] integer type
            #[9.2, 8.7, 8.2, 8.2, 8.5, 8.5]

        #Adding dummy values to test the negative result
        if userRequestedField.__eq__("Before"):
            values.append(3.5)
            values.append(2.8)
            values.append(1.6)
            values.append(2.5)
            values.append(4.8)
            values.append(3.6)

        if userRequestedField.__eq__("After"):
            values.append(7.5)
            values.append(9.8)
            values.append(10.6)
            values.append(12.5)
            values.append(13.8)
            values.append(15.6)

        return values

    def Run(self) -> Tuple[int, int]:
        # Get all before/after HbA1c readings
        old_Values = self._GetRequestedFields("Before")
        new_Values = self._GetRequestedFields("After")

        positiveCounts = 0
        negativeCounts = 0

        #Explaining the zip:
        #old_Values = [9.2, 8.4, 7.1] #new_Values = [7.1, 6.8, 6.5]
        #old_Values[0] compare new_Values[0]
        # 9.2 compare 7.1
        # 8.4 compare 6.8
        # 7.1 compare 6.5

        for oldResult,newResult in zip(old_Values, new_Values):
            if oldResult > newResult:
                positiveCounts += 1
            else:
                negativeCounts += 1

        self.result = (positiveCounts, negativeCounts)
        # Save the result inside the object
        return self.result

    def GetCaseName(self) -> str:
        return self.CaseName

    def CalculatePercentage(self) -> str:
        return f"The diabetes improvement is {ResultAnalyzer.CalculatePercentageBase(self.result):.2f}%"

    def TTestCalculator(self) -> str:
        oldValues = self._GetRequestedFields("Before")
        newValues = self._GetRequestedFields("After")

        tTestResult = ResultAnalyzer.TTestCalculatorBase(oldValues, newValues,self.CaseName)

        return tTestResult