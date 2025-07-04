from CommonStatisticTest.StatisticalTestCoordinator import StatisticalTestCoordinator
from StrategyCases import IStrategyHealthCase
from StrategyCases.DiabetesCase import DiabetesCase
from StrategyCases.HealthCaseStrategyHandler import HealthCaseStrategyHandler
from StrategyCases.HyperTensionCase import HyperTensionCase

def AnalyzeCase(iHealthCase:IStrategyHealthCase):
    healthCase = HealthCaseStrategyHandler(iHealthCase)
    results = healthCase.GetResultsCase()
    print(f"📊 {healthCase.GetCaseName()} Results:")
    print(f"✅ Positive Cases: {results[0]}")
    print(f"❌ Negative Cases: {results[1]}")
    print(f"📈 {healthCase.GetPercentage()}")
    print(f"\n{healthCase.GetTTestResult()}\n")
    cases = [HyperTensionCase(), DiabetesCase()]
    print(f"\n{StatisticalTestCoordinator.RunChiSquare(cases)}")
    print(f"\n{healthCase.GetLinearRegressionResult()}")


AnalyzeCase(HyperTensionCase())

AnalyzeCase(DiabetesCase())



#[64, 0]
#[72, 2]
#The diabetes improvement is 100%
#The hypertension improvement is 97.30%