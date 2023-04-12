import logging
from datetime import datetime, timedelta, timezone
import pygsheets
from copy import deepcopy

def write_df(df_metric, sh, sheet_name, delta, period, to_UTC=False):
    final_str = deepcopy(df_metric)
    final_str.fillna(value='', inplace=True)
    final_str.reset_index(inplace=True)
    write_data_to_gs_no_resize(final_str, sh, sheet_name, delta, period, to_UTC)

def write_update_time(delta, period, worksheet, to_UTC=False):
    """Write first line with current time and next upload"""
    if to_UTC:
        now = datetime.now(timezone.utc)
        tz = 'UTC +0'
    else:
        now = datetime.now()
        tz = 'UTC +3'
    now_str = now.strftime("%d.%m.%y %H:%M:%S")
    next_ = (now + timedelta(**{period:delta})).strftime("%d.%m.%y %H:%M:%S")
    worksheet.update_value("A1", "Last upload")
    worksheet.update_value("B1", f'{now_str} {tz}')
    worksheet.update_value("C1", "Next upload")
    worksheet.update_value("D1", f'{next_} {tz}')

def write_data_to_gs_no_resize(df,sh,worksheet_title,delta,period, to_UTC=False):
    worksheet = sh.worksheet_by_title(worksheet_title)
    worksheet.clear()
    write_update_time(delta,period, worksheet, to_UTC)
    worksheet.set_dataframe(df, "A2", copy_head=True)
    logging.warning(f'{worksheet.title} was updated')