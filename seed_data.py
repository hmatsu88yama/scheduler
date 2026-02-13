"""
テスト用サンプルデータ投入スクリプト
医員20人、外勤先10ヶ所を登録
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import init_db, add_doctor, add_clinic, set_affinity, get_doctors, get_clinics, update_clinic
import json
import random

init_db()

# 医員20人
doctor_names = [
    "田中太郎", "鈴木花子", "佐藤一郎", "山田二郎", "高橋三郎",
    "渡辺美咲", "伊藤健太", "中村由美", "小林誠", "加藤恵",
    "吉田裕子", "山本大輔", "松本直樹", "井上真理", "木村拓也",
    "林和也", "斎藤早紀", "清水浩二", "山口亮", "阿部綾乃",
]

for name in doctor_names:
    add_doctor(name)

# 外勤先10ヶ所
clinic_data = [
    ("A総合病院", 80000, "weekly"),
    ("Bクリニック", 60000, "weekly"),
    ("C医院", 50000, "weekly"),
    ("D病院", 70000, "biweekly_odd"),
    ("E診療所", 45000, "biweekly_even"),
    ("F総合病院", 90000, "weekly"),
    ("Gクリニック", 55000, "biweekly_odd"),
    ("H医院", 65000, "weekly"),
    ("I病院", 75000, "biweekly_even"),
    ("J診療所", 40000, "first_only"),
]

for name, fee, freq in clinic_data:
    add_clinic(name, fee, freq)

# 指名・相性をランダムに設定
doctors = get_doctors()
clinics = get_clinics()

random.seed(42)

for c in clinics:
    # 各外勤先に2-3人の指名
    preferred = random.sample([d["id"] for d in doctors], k=random.randint(2, 3))
    update_clinic(c["id"], preferred_doctors=preferred)

    # 相性スコア
    for d in doctors:
        if random.random() < 0.3:
            weight = round(random.uniform(1.0, 5.0), 1)
            set_affinity(d["id"], c["id"], weight)

print(f"サンプルデータ投入完了")
print(f"   医員: {len(doctors)}人")
print(f"   外勤先: {len(clinics)}ヶ所")
