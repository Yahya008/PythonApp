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
        self.hyperTensionsRows = DataPreprocessor.LoadCaseByConditionFromExcel("Condition", self.CaseName, self.requiredFields)

    #Private Method for the class
    def _GetRequestedFields(self, userRequestedField : str) -> list[float]:
        hyperTensionsValues = []

        for hyperTensionRow in self.hyperTensionsRows:
            before_bp = ValueParser.ParseBloodPressure(hyperTensionRow[f"BP_{userRequestedField}"])
            hyperTensionsValues.append(before_bp)
            #[160 , 100] integer type
            #systolic,diastolic = before_bp

        return hyperTensionsValues

    #Private Method for the class
    def _SplitBpValues(self, hyperTensionsValues) -> tuple[list[float],list[float]]:
        systolic = []
        diastolic = []
        for sys, dias in hyperTensionsValues:
            systolic.append(sys)
            diastolic.append(dias)

        return systolic, diastolic

    def Run(self) -> Tuple[int, int]:
        # Get all before/after blood pressure readings
        old_values = self._GetRequestedFields("Before")
        new_values = self._GetRequestedFields("After")

        # Split systolic and diastolic separately
        old_systolic, old_diastolic = self._SplitBpValues(old_values)
        new_systolic, new_diastolic = self._SplitBpValues(new_values)

        positiveCounts = 0
        negativeCounts = 0

        for i in range(len(old_systolic)):
            if new_systolic[i] < old_systolic[i] and new_diastolic[i] < old_diastolic[i]:
                positiveCounts += 1
            else:
                negativeCounts += 1

        self.result = (positiveCounts, negativeCounts)
        # Save the result inside the object
        return self.result

    def GetCaseName(self) -> str:
        return self.CaseName

    def CalculatePercentage(self) -> str:
        return f"The hypertension improvement is {ResultAnalyzer.CalculatePercentageBase(self.result):.2f}%"

    def TTestCalculator(self) -> str:
        oldValues = self._GetRequestedFields("Before")
        newValues = self._GetRequestedFields("After")

        oldSystolicValues, oldDiastolicValues = self._SplitBpValues(oldValues)

        newSystolicValues, newDiastolicValues = self._SplitBpValues(newValues)

        sysTTestResult = ResultAnalyzer.TTestCalculatorBase(oldSystolicValues, newSystolicValues,
                                                            self.CaseName + " Systolic")
        diasTTestResult = ResultAnalyzer.TTestCalculatorBase(oldDiastolicValues, newDiastolicValues,
                                                             self.CaseName + " Diastolic")

        finalTTestResult = f"{sysTTestResult}\n\n{diasTTestResult}"

        return finalTTestResult