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
    print(f"\n{healthCase.GetAnovaTestResult('Gender','After')}")

AnalyzeCase(HyperTensionCase())
AnalyzeCase(DiabetesCase())

diabetesGenderFilter = DiabetesCase().GroupRowsByColumnValueNew("Gender","HbA1c_After",
                                               conditionFilter={"Column": "Condition", "Value":"Diabetes"})

# print("Male:")
# print(diabetesGenderFilter['Male'])
# print("Female:")
# print(diabetesGenderFilter['Female'])

hyperTensionGenderFilter = HyperTensionCase()._GroupBpByColumn("Gender", "BP_After",
                                                               conditionFilter={"Column": "Condition", "Value":"Hypertension"})

hypertension = HyperTensionCase()

print("📊 ANOVA: Systolic grouped by Gender")
print(hypertension.AnovaTestBy("Gender", "After"))

print("\n📊 ANOVA: Diastolic grouped by Age")
print(hypertension.AnovaTestBy("Age", "After"))

#Tested values to check if everything is correct
#diabetes cases:[64, 0]
#hypertension cases:[72, 2]
#The diabetes improvement is 100%
#The hypertension improvement is 97.30%