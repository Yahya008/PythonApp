class ValueParser:
    @staticmethod
    def StripRemover(value):
        return float(str(value).strip("%"))
    #8.9%=>8.9(float)

    @staticmethod
    def ParseBloodPressure(bp):
        systolic,diastolic = map(int,bp.split("/"))
        return [systolic,diastolic]









    # Before: 160 / 100
    # After: 124 / 87

    # ["160" , "100" ] => Type is string
    # int.Parse(160) int(100) => [160 , 100] =>Type is integer
    # mapping [160 , 100 , 80]=> before_systolic = 160