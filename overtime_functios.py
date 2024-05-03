from datetime import timedelta
import streamlit as st
from dateutil import rrule

config = st.session_state.config
period = st.session_state.period


# Cuando el empleado trabaja de noche y las horas de la semana no superan las 47
def calculate_night_surcharges_hours(
    hour_rate, entry_datetime, worked_hours, day_key, holidays, total_week_hours
):
    night_surcharges_hours = 0
    night_holidays_surcharges_hours = 0

    if day_key != 10 and day_key != 12 and day_key not in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours > config.getint(period, "max_hours_per_week"):
                continue
            elif hour_day.hour > config.getint(period, "start_night_limit"):
                night_surcharges_hours += 1
            elif (
                day_key + 2 in holidays
                and hour_day.hour > 0
                and hour_day.hour < config.getint(period, "end_night_limit")
            ):
                night_holidays_surcharges_hours += 1
            elif night_surcharges_hours > 0 and hour_day.hour < config.getint(
                period, "end_night_limit"
            ):
                night_surcharges_hours += 1
            total_week_hours += 1

    elif day_key == 10 and day_key not in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours > config.getint(period, "max_hours_per_week"):
                continue
            elif hour_day.hour > config.getint(period, "start_night_limit"):
                night_surcharges_hours += 1
            elif night_surcharges_hours > 0 and hour_day.hour <= 0:
                night_surcharges_hours += 1
            elif hour_day.hour > 0 and hour_day.hour < config.getint(period, "end_night_limit"):
                night_holidays_surcharges_hours += 1
            total_week_hours += 1

    elif day_key in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours > config.getint(period, "max_hours_per_week"):
                continue
            elif hour_day.hour > config.getint(period, "start_night_limit"):
                night_holidays_surcharges_hours += 1
            elif night_holidays_surcharges_hours > 0 and hour_day.hour <= 0:
                night_holidays_surcharges_hours += 1
            elif (
                day_key + 2 in holidays
                and hour_day.hour > 0
                and hour_day.hour < config.getint(period, "end_night_limit")
            ):
                night_holidays_surcharges_hours += 1
            elif (
                day_key + 2 not in holidays
                and hour_day.hour > 0
                and hour_day.hour < config.getint(period, "end_night_limit")
            ):
                night_surcharges_hours += 1
            total_week_hours += 1

    night_surchage_pay = round(
        night_surcharges_hours * hour_rate * config.getfloat(period, "night_surcharges")
    )
    night_holidays_surchage_pay = round(
        night_holidays_surcharges_hours
        * hour_rate
        * config.getfloat(period, "night_holidays_surcharges")
    )

    return (
        night_surchage_pay,
        night_surcharges_hours,
        night_holidays_surchage_pay,
        night_holidays_surcharges_hours,
    )


# Cuando el empleado trabaja de dia en dom- festivo y las horas de la semana no superan las 47
def calculate_day_surcharges_hour(
    hour_rate, entry_datetime, worked_hours, day_key, holidays, total_week_hours
):
    holidays_surchage_hour = 0
    if day_key in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours > config.getint(period, "max_hours_per_week"):
                continue
            elif hour_day.hour > config.getint(
                period, "end_night_limit"
            ) and hour_day.hour < config.getint(period, "start_night_limit"):
                holidays_surchage_hour += 1
            total_week_hours += 1

    holidays_surchage_pay = round(
        holidays_surchage_hour * hour_rate * config.getfloat(period, "day_holidays_surcharges")
    )

    return holidays_surchage_hour, holidays_surchage_pay


# calculo de las horas extra noctunas nomal y noc en dominicales y festivos
def calculate_night_overtime_and_holydays(
    hour_rate, entry_datetime, worked_hours, day_key, holidays, total_week_hours
):
    night_overtime_hours = 0
    night_holidays_overtime_hours = 0

    if day_key != 10 and day_key != 12 and day_key not in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours <= config.getint(period, "max_hours_per_week"):
                total_week_hours += 1
            elif hour_day.hour > config.getint(period, "start_night_limit"):
                night_overtime_hours += 1
            elif (
                day_key + 2 in holidays
                and hour_day.hour > 0
                and hour_day.hour < config.getint(period, "end_night_limit")
            ):
                night_holidays_overtime_hours += 1
            elif night_overtime_hours > 0 and hour_day.hour < config.getint(
                period, "end_night_limit"
            ):
                night_overtime_hours += 1

    elif day_key == 10 and day_key not in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours <= config.getint(period, "max_hours_per_week"):
                total_week_hours += 1
            elif hour_day.hour > config.getint(period, "start_night_limit"):
                night_overtime_hours += 1
            elif night_overtime_hours > 0 and hour_day.hour <= 0:
                night_overtime_hours += 1
            elif hour_day.hour > 0 and hour_day.hour < config.getint(period, "end_night_limit"):
                night_holidays_overtime_hours += 1

    elif day_key in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours <= config.getint(period, "max_hours_per_week"):
                total_week_hours += 1
            elif hour_day.hour > config.getint(period, "start_night_limit"):
                night_holidays_overtime_hours += 1
            elif night_holidays_overtime_hours > 0 and hour_day.hour <= 0:
                night_holidays_overtime_hours += 1
            elif (
                day_key + 2 in holidays
                and hour_day.hour > 0
                and hour_day.hour < config.getint(period, "end_night_limit")
            ):
                night_holidays_overtime_hours += 1
            elif (
                day_key + 2 not in holidays
                and hour_day.hour > 0
                and hour_day.hour < config.getint(period, "end_night_limit")
            ):
                night_overtime_hours += 1

    night_overtime_pay = round(
        night_overtime_hours * (hour_rate + (hour_rate * config.getfloat(period, "night_overtime")))
    )
    night_holidays_overtime_pay = round(
        night_holidays_overtime_hours
        * (hour_rate + (hour_rate * config.getfloat(period, "night_overtime")))
    )

    return (
        night_overtime_pay,
        night_overtime_hours,
        night_holidays_overtime_pay,
        night_holidays_overtime_hours,
    )


# calculo de las horas extras diurnas en dom-fes
def calculate_daytime_holidays_hour(
    hour_rate, entry_datetime, worked_hours, day_key, holidays, total_week_hours
):
    daytime_holidays_hours = 0
    if day_key in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours <= config.getint(period, "max_hours_per_week"):
                total_week_hours += 1
            elif hour_day.hour > config.getint(
                period, "end_night_limit"
            ) and hour_day.hour < config.getint(period, "start_night_limit"):
                daytime_holidays_hours += 1

    daytime_holidays_pay = round(
        daytime_holidays_hours
        * (hour_rate + (hour_rate * config.getfloat(period, "daytime_holidays")))
    )

    return daytime_holidays_hours, daytime_holidays_pay


# calculo de horas extra normal
def calculate_daytime_overtime(
    hour_rate, entry_datetime, worked_hours, day_key, holidays, total_week_hours
):
    daytime_overtime_hours = 0

    if day_key != 10 and day_key != 12 and day_key not in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours <= config.getint(period, "max_hours_per_week"):
                total_week_hours += 1
            elif hour_day.hour > config.getint(
                period, "end_night_limit"
            ) and hour_day.hour < config.getint(period, "start_night_limit"):
                daytime_overtime_hours += 1

    elif day_key == 10 and day_key not in holidays:
        for hour_day in rrule.rrule(
            rrule.HOURLY,
            dtstart=entry_datetime,
            until=entry_datetime + timedelta(hours=worked_hours),
        ):
            if total_week_hours <= config.getint(period, "max_hours_per_week"):
                total_week_hours += 1
            elif hour_day.hour > config.getint(
                period, "end_night_limit"
            ) and hour_day.hour < config.getint(period, "start_night_limit"):
                daytime_overtime_hours += 1

    daytime_overtime_pay = round(
        daytime_overtime_hours
        * (hour_rate + (hour_rate * config.getfloat(period, "daytime_overtime")))
    )

    return daytime_overtime_hours, daytime_overtime_pay
