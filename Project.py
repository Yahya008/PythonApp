from CommonStatisticTest.StatisticalTestCoordinator import StatisticalTestCoordinator
from StrategyCases import IStrategyHealthCase
from StrategyCases.DiabetesCase import DiabetesCase
from StrategyCases.HealthCaseStrategyHandler import HealthCaseStrategyHandler
from StrategyCases.HyperTensionCase import HyperTensionCase

print("Another way")

def AnalyzeCase(iHealthCase:IStrategyHealthCase):
    healthCase = HealthCaseStrategyHandler(iHealthCase)
    results = healthCase.GetResultsCase()
    print(f"📊 {healthCase.GetCaseName()} Results:")
    print(f"✅ Positive Cases: {results[0]}")
    print(f"❌ Negative Cases: {results[1]}")
    print(f"📈 {healthCase.GetPercentage()}")
    print(f"\n{healthCase.GetTTestResult()}\n")
    print(f"{healthCase.GetLinearRegressionResult()}")

#print(DiabetesCase().TTestCalculator())
AnalyzeCase(HyperTensionCase())
#print(HyperTensionCase().TTestCalculator())

print("\n\n\n")

print(AnalyzeCase(DiabetesCase()))
#
# lists = [DiabetesCase(),HyperTensionCase()]
#
# chi_result = StatisticalTestCoordinator.RunChiSquare(lists)
# print(chi_result)

#[64, 0]
#[72, 2]
#The diabetes improvement is 100%
#The hypertension improvement is 97.30%