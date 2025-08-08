import os
from flask import Blueprint, render_template, request, jsonify
from app.utils.data_loader import load_patient_info, get_patient_list, get_patient_info
from app.utils.image_processing import match_image_to_patient
from app.utils.visualization import generate_charts

main_bp = Blueprint('main', __name__)

# Đường dẫn đến thư mục ảnh
IMAGE_FOLDER = ''

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/predict', methods=['POST'])
def predict():
    patient_id = request.form.get('patient_id')

    if not patient_id:
        return render_template('error.html', message="Please enter a valid Patient ID")

    patient_info = get_patient_info(patient_id)

    if not patient_info:
        return render_template('error.html', message="Patient not found")
    
    image_files = { 
        "flair": os.path.join(IMAGE_FOLDER, f"{patient_info['flair']}"),
        "seg": os.path.join(IMAGE_FOLDER, f"{patient_info['seg']}"),
        "t1": os.path.join(IMAGE_FOLDER, f"{patient_info['t1']}"),
        "t1ce": os.path.join(IMAGE_FOLDER, f"{patient_info['t1ce']}"),
        "t2": os.path.join(IMAGE_FOLDER, f"{patient_info['t2']}"),
    }

    # Kiểm tra nếu đường dẫn ảnh tồn tại, nếu không trả về thông báo lỗi
    for key, image_path in image_files.items():
        if not os.path.exists(image_path):
            print(f"Error: Image for {key} not found at {image_path}")

    # Xử lý ảnh và lấy kết quả
    result = match_image_to_patient()

    if result.get("active_contour") is None:
        result["active_contour"] = ""

    return render_template('predict.html', patient=patient_info, result=result, images = image_files)

@main_bp.route('/filter', methods=['GET'])
def filter_patients():
    grade = request.args.get('grade')
    tumor = request.args.get('tumor')
    patients = get_patient_list(grade, tumor)
    return render_template('filter.html', patients=patients)

@main_bp.route('/stats', methods=['GET'])
def stats():
    grade_filter = request.args.get('grade')
    tumor_filter = request.args.get('tumor')

    if not grade_filter or not tumor_filter:
        return render_template('error.html', message="Missing grade or tumor filter")

    charts, bar_data, pie_data, line_data = generate_charts(grade_filter, tumor_filter)

    return render_template('stats.html', 
                           charts=charts,
                           bar_data=bar_data,
                           pie_data=pie_data,
                           line_data=line_data)




