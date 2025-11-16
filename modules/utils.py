from io import BytesIO
import pandas as pd
def export_multiple_sheets(sheets_dict):
    """
    sheets_dict = {"SheetName": dataframe, ...}
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in sheets_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])  # Excel limit 31 chars
    return output.getvalue()