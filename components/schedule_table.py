"""スケジュール表の共通表示コンポーネント"""
import streamlit as st
import pandas as pd
from datetime import date


def render_schedule_table(sched, doctors, clinics):
    """スケジュールをカレンダー形式のテーブルで表示する"""
    doc_map = {d["id"]: d["name"] for d in doctors}
    clinic_map = {c["id"]: c["name"] for c in clinics}

    cal_data = {}
    for a in sched["assignments"]:
        ds = a["date"]
        cname = clinic_map.get(a["clinic_id"], "?")
        dname = doc_map.get(a["doctor_id"], "?")
        if ds not in cal_data:
            cal_data[ds] = {}
        cal_data[ds][cname] = dname

    if not cal_data:
        return None

    dates_sorted = sorted(cal_data.keys())
    all_clinic_names = sorted(set(
        cn for day_data in cal_data.values() for cn in day_data.keys()
    ))

    rows = []
    for cn in all_clinic_names:
        row = {"外勤先": cn}
        for ds in dates_sorted:
            d_obj = date.fromisoformat(ds)
            col_name = d_obj.strftime("%m/%d(%a)")
            row[col_name] = cal_data.get(ds, {}).get(cn, "-")
        rows.append(row)

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    return df
