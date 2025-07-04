import pandas as pd

class DataPreprocessor:
    @staticmethod
    def LoadCaseByConditionFromExcel(column: str, value: str, requiredFields : list):
        path = r"C:\Users\YAHYA\\Desktop\herbal_medicine_large_mock_data.xlsx"
        excelFile = pd.read_excel(path)

        #1 Filter rows
        filtered = excelFile[excelFile[column] == value]

        # 2. Extract row data only
        rows = DataPreprocessor.ExtractRowsFields(filtered)

        # 3. Validate required fields
        DataPreprocessor.ValidateRequiredFields(rows, requiredFields)

        return rows

    @staticmethod
    def ExtractRowsFields(dataFrame):
        """
        Takes a pandas DataFrame.iterrows() generator and extracts only the row values (ignores the index).
        Returns a list of rows (Series objects).
        """
        return [row for _, row in dataFrame.iterrows()]

    # To ask him about if there is any missing values
    @staticmethod
    def ValidateRequiredFields(rows, fields: list):
        for row in rows:
            for field in fields:
                value = row.get(field)
                if pd.isna(value) or value is None or (isinstance(value, str) and value.strip() == ""):
                    raise ValueError(f"Missing required filed '{field}' in patient ID {row.get('Patient_ID')}")

