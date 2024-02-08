from tools import log_message, get_or_create_money_style
import streamlit as st


def simple_sheet_process(workbook):
    extracted_data = st.session_state.extracted_data

    # Select Sheets
    if "Simple Sheet" in workbook.sheetnames:
        log_message("processing simple sheet")
        simple_sheet = workbook["Simple Sheet"]

        processed_first_week = False

        for week_name, week_data in extracted_data.items():
            if not processed_first_week:
                for employee_name, employee_info in week_data.items():
                    salary = employee_info["salary"]
                    simple_sheet.append([employee_name, salary])
                processed_first_week = True

        variables = {
            "total_hours": 3,
            "night_surchage_hours": 4,
            "night_surchage_pay": 5,
            "day_holidays_surcharges_hours": 6,
            "day_holidays_surchage_pay": 7,
            "night_holidays_surcharges_hours": 8,
            "night_holidays_surchage_pay": 9,
            "daytime_overtime_hours": 10,
            "daytime_overtime_pay": 11,
            "night_overtime_hours": 12,
            "night_overtime_pay": 13,
            "daytime_holidays_hours": 14,
            "daytime_holidays_pay": 15,
            "night_holidays_overtime_hours": 16,
            "night_holidays_overtime_pay": 17,
            "total_weeks": 18,
        }

        for row_index in range(2, simple_sheet.max_row + 1):
            for var_name, column in variables.items():
                formula = "="
                for sheet in workbook.sheetnames:
                    if sheet.startswith("week"):
                        current_sheet = workbook[sheet]
                        formula += f"VLOOKUP(A{row_index}, '{current_sheet.title}'!$A$2:$R${current_sheet.max_row}, {column}, FALSE)+"

                formula = formula.rstrip("+")
                simple_sheet.cell(row=row_index, column=column, value=formula)

        money_style = get_or_create_money_style(workbook)
        for col in ["B", "E", "G", "I", "K", "M", "O", "Q", "R"]:
            for cell in simple_sheet[col]:
                cell.style = money_style
                cell.number_format = "$#,##0"

    return workbook


def main(workbook, progress_bar):
    simple_sheet_process(workbook)

    if progress_bar is not None:
        progress_bar.progress(1.0)

    return workbook
