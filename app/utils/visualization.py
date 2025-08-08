import matplotlib.pyplot as plt
import io
import base64
from flask import Markup
from app.utils.data_loader import get_patient_list

def generate_charts(grade_filter, tumor_filter):
    patients_df = get_patient_list(grade=grade_filter, tumor=tumor_filter)
    patients_list = patients_df 

    if not patients_list:
        return None, {}, {}, {}

    years = ["2018", "2019", "2020"]
    year_counts = {year: 0 for year in years}

    for patient in patients_list:
        year = str(patient["Year"])
        if year in year_counts:
            year_counts[year] += 1

    # Tạo JSON cho Chart.js
    bar_data = {
        "labels": list(year_counts.keys()),
        "datasets": [{
            "label": "Patient Count",
            "data": list(year_counts.values()),
            "backgroundColor": ["red", "blue", "green"]
        }]
    }

    pie_data = {
        "labels": list(year_counts.keys()),
        "datasets": [{
            "data": list(year_counts.values()),
            "backgroundColor": ["red", "blue", "green"]
        }]
    }

    line_data = bar_data  # Dùng chung dữ liệu với biểu đồ cột

    return None, bar_data, pie_data, line_data  # Trả về JSON thay vì hình ảnh
