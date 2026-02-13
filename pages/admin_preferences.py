"""管理者: 希望状況一覧タブ"""
import streamlit as st
import pandas as pd
from database import get_doctors, get_all_preferences
from optimizer import get_target_saturdays


def render(target_month, year, month):
    st.header(f"希望状況一覧 ({target_month})")

    doctors = get_doctors()
    prefs = get_all_preferences(target_month)
    pref_map = {p["doctor_id"]: p for p in prefs}

    saturdays = get_target_saturdays(year, month)
    sat_strs = [s.strftime("%m/%d") for s in saturdays]

    if doctors:
        data = []
        for d in doctors:
            p = pref_map.get(d["id"])
            row = {"医員": d["name"], "入力済": "済" if p else "-"}
            if p:
                ng = set(p.get("ng_dates", []))
                avoid = set(p.get("avoid_dates", []))
                for s, s_str in zip(saturdays, sat_strs):
                    ds = s.isoformat()
                    if ds in ng:
                        row[s_str] = "×"
                    elif ds in avoid:
                        row[s_str] = "△"
                    else:
                        row[s_str] = "○"
            else:
                for s_str in sat_strs:
                    row[s_str] = "-"
            data.append(row)

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        submitted = sum(1 for _ in pref_map.values())
        st.info(f"入力済: {submitted}/{len(doctors)}人")
    else:
        st.warning("医員が登録されていません。マスタ管理で追加してください。")
