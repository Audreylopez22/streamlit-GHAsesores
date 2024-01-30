import streamlit as st
import datetime
from datetime import datetime
from openpyxl.styles import NamedStyle

def log_message(message):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    st.text(f"[{formatted_time}] {message}")
    
def get_or_create_money_style(workbook):
    money_style_name = 'money'
    
    # # Check if the 'money' style already exists
    for style in workbook._named_styles:
        if style.name == money_style_name:
            return style

    # If it does not exist, create and add the style 'money'.
    money_style = NamedStyle(name=money_style_name, number_format='"$"#,##0.00')
    workbook.add_named_style(money_style)
    
    return money_style