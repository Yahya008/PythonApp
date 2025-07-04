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

    # Private Method for the class
    def _GetSplitSystolicAndDiastolic(self) -> Tuple[list[float], list[float], list[float], list[float]]:
        # Get all before/after blood pressure readings
        old_Values = self._GetRequestedFields("Before")
        new_Values = self._GetRequestedFields("After")

        # Split systolic and diastolic separately
        old_Systolic, old_Diastolic = self._SplitBpValues(old_Values)
        new_Systolic, new_Diastolic = self._SplitBpValues(new_Values)

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
        # Save the result inside the object
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
        old_Values = self._GetRequestedFields("Before")
        new_Values = self._GetRequestedFields("After")

        old_Systolic, old_Diastolic = self._SplitBpValues(old_Values)
        new_Systolic, new_Diastolic = self._SplitBpValues(new_Values)

        systolicResult = ResultAnalyzer.LinearRegressionBase(old_Systolic, new_Systolic, self.CaseName)

        diastolicResult = ResultAnalyzer.LinearRegressionBase(old_Diastolic, new_Diastolic,self.CaseName)

        return systolicResult + "\n\n" + diastolicResult