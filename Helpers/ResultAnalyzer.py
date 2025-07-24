from sklearn.linear_model import LinearRegression
from scipy.stats import ttest_rel
from scipy.stats import chi2_contingency
from scipy.stats import f_oneway
import numpy as np

class ResultAnalyzer:
    @staticmethod
    def CalculatePercentageBase(listOfResults):
        totalCases = listOfResults[0] + listOfResults[1]

        percentageImprovement = (listOfResults[0] / totalCases) * 100

        return percentageImprovement

    @staticmethod
    def TTestCalculatorBase(allBeforeValues,allAfterValues,caseName) -> str:
        allBefore = allBeforeValues
        allAfter = allAfterValues

        if len(allBefore) < 2:
            return f"Not enough data to run T-Test for {caseName}."

        t_stat, p_val = ttest_rel(allBefore, allAfter)

        result = (
            f"📊 {caseName} T-Test Results:\n"
            f"📈 t-statistic: {t_stat:.8f}\n"
            f"📉 p-value: {p_val:.8f}\n"
        )

        if p_val < 0.05:
            result += "✅ Statistically significant improvement!"
        else:
            result += "❌ There is no statistically significant improvement."

        return result

    @staticmethod
    def ChiSquareTestBase(healthCaseData) -> str:
        chi2, p , dof, expected = chi2_contingency(healthCaseData)

        result = (
            f"📊 Chi-Square Test Results:\n"
            f"χ²-statistic: {chi2:.4f}\n"
            f"Degrees of Freedom: {dof}\n"
            f"p-value: {p:.4f}\n"
        )

        if p < 0.05:
            result += "✅ Statistically significant association!"
        else:
            result += "❌ No statistically significant association."

        return result

    @staticmethod
    def LinearRegressionBase(allBeforeValues,allAfterValues,caseName) -> str:
        if len(allBeforeValues) < 2:
            return f"Not enough data to run Linear Regression for {caseName}."

        x = np.array(allBeforeValues).reshape(-1, 1)
        y = np.array(allAfterValues)

        model = LinearRegression()
        model.fit(x,y)

        slope = model.coef_[0]
        intercept = model.intercept_
        r_squared = model.score(x, y)

        result = (
            f"📊 Linear Regression for {caseName}:\n"
            f"🧮 Equation: y = {slope:.4f}x + {intercept:.4f}\n"
            f"📈 R-squared: {r_squared:.4f}\n"
        )

        if r_squared > 0.7:
            result += "✅ Strong linear relationship."
        elif r_squared > 0.4:
            result += "⚠️ Moderate linear relationship."
        else:
            result += "❌ Weak or no linear relationship."

        return result

    @staticmethod
    #*groups: list[float]=>Accept multiple list[float] arguments
    def AnovaTestBase(*groupsOfValues:list[float]) -> str:
        if len(groupsOfValues) < 2:
            return "Not enough data need at least 2 groups for ANOVA test."

        # Check if each group has at least 2 values
        if any(len(group) < 2 for group in groupsOfValues):
            return "Each group must have at least 2 data points."

        f_stat, p_val = f_oneway(*groupsOfValues)

        result = (
            f"📊 ANOVA Test Results:\n"
            f"🧪 F-statistic: {f_stat:.4f}\n"
            f"📉 p-value: {p_val:.4f}\n"
        )

        if p_val < 0.05:
            result += "✅ At least one group has a significantly different mean."
        else:
            result += "❌ No significant difference between group means."

        return result