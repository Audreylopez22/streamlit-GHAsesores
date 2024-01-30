from datetime import datetime, timedelta
from tools import log_message
import streamlit as st
from dateutil import rrule
from overtime_functios import calculate_night_surcharges_hours, daytime_overtime_per_week,calculate_day_surcharges_hour

config=st.session_state.config
period=st.session_state.period

#st.write(config)
#st.write(period)

def define_weeks(sheet):
    tables_info=[]
    weeks_info=[]
    start_week= ""
    colaborador= ""
    holidays=[]
    names=[]
    salary=[]
    hour_rate= []
    max_hours_per_month = config.getint(period, 'max_hours_per_month')
    
    for (row1,row2) in zip(sheet.iter_rows(min_col=1, max_col=1,min_row=1, max_row=sheet.max_column),sheet.iter_rows(min_col=2, max_col=2,min_row=1, max_row=sheet.max_column)):
        for (cell1, cell2) in zip(row1,row2):
 
            if cell1.value is not None and str(cell1.value) == 'Colaborador':
                colaborador = cell1.row
                
            elif cell1.value is None and colaborador != "":
                tables_info.append({
                    "row_min": colaborador -1,
                    "row_max": cell1.row -1 ,
                    "names": names,
                    "salary": salary,
                    "hour_rate": hour_rate
                })

                colaborador= ""
                names= []
                salary=[]
                hour_rate= []
                
            elif cell1.value is not None:
                names.append(cell1.value)
                if cell2.value is not None:
                    salary.append(cell2.value)
                    hour_rate.append(round(cell2.value/max_hours_per_month))
                    
    
    #st.write(tables_info)
                
    #esto me da las semanas de trabajo 
    for tableinfo in tables_info:
        
        for columna in sheet.iter_cols(min_row=tableinfo["row_min"], max_row=tableinfo["row_min"]):
            for celda in columna:

                if celda.value is not None and str(celda.value).startswith('Lunes'):
                    #cambiar a inicio de semana en ingles 
                    start_week = celda.column
                    
                if celda.value is not None and start_week and start_week <= celda.column < start_week + 15 and celda.fill.start_color.rgb != '00000000':
                        holidays.append(celda.column)
                    
                if celda.value is not None and str(celda.value).startswith('Domingo') and start_week != "":
                    weeks_info.append({
                        "row_min": tableinfo["row_min"]+2,
                        "row_max": tableinfo["row_max"],
                        "col_min": start_week,
                        "col_max": celda.column + 1,
                        "names": tableinfo["names"],
                        "salary": tableinfo["salary"],
                        "hour_rate": tableinfo["hour_rate"],
                        "holidays": holidays
                    }) 
                    start_week= ""
                    holidays= []
                    
    #st.write("tables_info")
    #st.write(tables_info)
    # st.write("weeks_info")
    #st.write(weeks_info)     
    return weeks_info, tables_info

def extract_data(sheet, weeks_info):
    extracted_data= {}
    
    for week_info in weeks_info:
        
        week_name="week {}".format(len(extracted_data)+1)
        extracted_data[week_name]={}
        key_row=0
        
        for row in sheet.iter_rows(min_col=week_info["col_min"], max_col=week_info["col_max"],min_row=week_info["row_min"], max_row=week_info["row_max"], values_only=True ):
            
            
            employe_name= week_info["names"][key_row]
            employe_salary= week_info["salary"][key_row]
            hour_rate= week_info["hour_rate"][key_row]
            
            holidays=[h-week_info["col_min"] for h in week_info["holidays"]]
            
            total_week_hours = 0 
            daytime_overtime= 0
            #recargos nocturnos
            night_surchage_week= 0
            total_night_surcharges=0
            #recargos dom-fes nocturnos
            total_night_holidays_surcharges= 0
            night_holidays_surchage_week=0
            # recargo de dom-fest dia 
            total_holidays_surchages=0
            holidays_surchage_week=0
            
            #st.write(employe_name)
            for i in range (0,len(list(row)),2):
                  
                if row[i] and row[i + 1]:
                    try: 
                        entry_datetime = datetime.strptime(str(row[i]), "%H:%M:%S") if row[i] else None
                        exit_datetime = datetime.strptime(str(row[i + 1]), "%H:%M:%S") if row[i + 1] else None
                        
                    except Exception as error:
                        print(error)
                        continue
                    worked_hours = abs((exit_datetime - entry_datetime).total_seconds() / 3600)
                    
                    #CUIDADO AQUI NO TIENE EN CUENTA SI LOS RECARGOS NOCTURNOS SON FESTIVOS
                    night_surchage_pay,night_surcharges_hours, night_holidays_surchage_pay,night_holidays_surcharges_hours=calculate_night_surcharges_hours(hour_rate,entry_datetime,worked_hours,i,holidays)
                    #night normal week surcharges
                    night_surchage_week += night_surchage_pay
                    total_night_surcharges+=night_surcharges_hours
                    #night holidays surcharges
                    total_night_holidays_surcharges += night_holidays_surchage_pay
                    night_holidays_surchage_week += night_holidays_surcharges_hours
                    
                    

                    # st.write("worked_hours")
                    # st.write(worked_hours)
                    # st.write(night_surchage_pay)
                    # st.write("night_surcharges_hours")
                    # st.write(night_surcharges_hours)
                    # st.write(night_holidays_surchage_pay)
                    # st.write(night_holidays_surcharges_hours)
                    
                    holidays_surchage_hour, holidays_surchage_pay=calculate_day_surcharges_hour(hour_rate,entry_datetime,worked_hours, i,holidays)
                    
                    #day holidays surcharges
                    
                    total_holidays_surchages += holidays_surchage_pay
                    holidays_surchage_week += holidays_surchage_hour
                    
                    # st.write("holidays_surchage_hour")
                    # st.write(holidays_surchage_hour)
                    # st.write("holidays_surchage_week")
                    # st.write(holidays_surchage_week)
                    # st.write("holidays_surchage_pay")
                    # st.write("total_holidays_surchages")
                    # discount for lunch after max_hours_discount_lunch in config.ini
                    if worked_hours >= config.getint(period, 'max_hours_discount_lunch'):
                        worked_hours= worked_hours-1
                        
                    total_week_hours += worked_hours
                    
                    #Trae el limite de horas por semana del archivo de configuracion
                    if total_week_hours> config.getint(period, 'max_hours_per_week'):
                        #se calcula hora extra diruna
                        #se calcula hora extra nocturna
                        #se calcula hora extra festiva 
                        extra_hour= total_week_hours-config.getint(period, 'max_hours_per_week')
                        daytime_overtime= round(daytime_overtime_per_week(hour_rate)*extra_hour)
                        
                    extracted_data[week_name][employe_name] = {
                        "hour_rate": hour_rate,
                        "salary": employe_salary,
                        "total_hours": total_week_hours,
                        "night_surchage_hours": total_night_surcharges,
                        "night_surchage_pay" : night_surchage_week,
                        "night_holidays_surcharges_hours": night_holidays_surchage_week,
                        "night_holidays_surchage_pay": total_night_holidays_surcharges,
                        "day_holidays_surcharges_hours":holidays_surchage_week,
                        "day_holidays_surchage_pay": total_holidays_surchages
                        
                    }
                    
                    #st.write(extracted_data)    
                
            key_row +=1
    #st.write(extracted_data)
    st.session_state['extracted_data']= extracted_data
    log_message("The information was compiled by workweek.")



def main(workbook, progress_bar):
    for sheet in workbook:
        weeks_info, tables_info= define_weeks(sheet)
        extract_data(sheet, weeks_info)
        break
    
    if progress_bar is not None:
        progress_bar.progress(1.0)

    return workbook
