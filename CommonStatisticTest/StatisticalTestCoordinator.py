from Helpers.ResultAnalyzer import ResultAnalyzer
from StrategyCases.IStrategyHealthCase import IStrategyHealthCase


class StatisticalTestCoordinator:
    @staticmethod
    def RunChiSquare(cases:list[IStrategyHealthCase]) -> str:
        data = []
        for case in cases:
            result = case.Run() # To get the (positive,negative)(72,2),(64,0)
            data.append(list(result))

        #data[0] = (64,0)
        #data[1] = (72,2)

        return ResultAnalyzer.ChiSquareTestBase(data)