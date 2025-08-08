import numpy as np
import os
import cv2
import csv
from skimage import filters
from random import choice
from skimage.measure import label
from sklearn.metrics import accuracy_score
from skimage.segmentation import active_contour
from app.utils.data_loader import get_patient_info

# So sánh sự tương đồng giữa ground truth và dự đoán (có thể là seg_binary)
# ground_truth là ảnh phân vùng thật sự (có thể là ảnh mask), prediction là ảnh phân vùng đã được xử lý
# Ta sử dụng phương pháp accuracy_score của sklearn để tính toán độ chính xác
def calculate_accuracy(ground_truth, prediction):
    ground_truth_flat = ground_truth.flatten()
    prediction_flat = prediction.flatten()

    return accuracy_score(ground_truth_flat, prediction_flat)

def match_image_to_patient(image_file=None):
    dataset_path = "static/images/Dataset"
    
    if not os.path.exists(dataset_path):
        return {"error": "Dataset path does not exist", "active_contour": None}

    patient_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    
    if not patient_dirs:
        return {"error": "No patient directories found", "active_contour": None}
    
    random_patient = choice(patient_dirs)
    patient_info = get_patient_info(random_patient)

    if not patient_info:
        return {"error": "Patient information not found", "active_contour": None}

    flair_path = os.path.join(dataset_path, random_patient, "flair.png")
    seg_path = os.path.join(dataset_path, random_patient, "seg.png")

    flair_image = cv2.imread(flair_path)
    seg_image = cv2.imread(seg_path)

    if flair_image is None or seg_image is None:
        return {"error": "Failed to read images", "active_contour": None}

    seg_gray = cv2.cvtColor(seg_image, cv2.COLOR_BGR2GRAY)
    threshold = filters.threshold_otsu(seg_gray)
    seg_binary = seg_gray > threshold

    s = np.linspace(0, 2 * np.pi, 400)
    init = np.array([100 + 50 * np.cos(s), 100 + 50 * np.sin(s)]).T

    try:
        active_contour_image = active_contour(seg_binary, init)
        tumor_present = "yes" if np.any(seg_binary) else "no"

        active_contour_path = os.path.join("static/img", f"{random_patient}_active_contour.jpg")
        active_contour_dir = os.path.dirname(active_contour_path)
        if not os.path.exists(active_contour_dir):
            os.makedirs(active_contour_dir)
        
        if active_contour_image is None:
            return {"error": "Failed to generate active contour", "active_contour": None}

        cv2.imwrite(active_contour_path, active_contour_image)
        
        # Tính toán độ chính xác
        # Giả sử ground truth là seg_binary hoặc mask thực tế từ dữ liệu
        ground_truth = seg_binary
        accuracy = calculate_accuracy(ground_truth, active_contour_image)  # So sánh ground_truth với ảnh active contour

    except Exception as e:
        return {"error": f"Active contour processing failed: {str(e)}", "active_contour": None}

    year = random_patient[:7]
    log_path = f"data/log_info_{year}.csv"
    log_data = [random_patient, patient_info["tumor"], tumor_present, accuracy]

    with open(log_path, mode='a', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(log_data)

    return {
        "active_contour": active_contour_path,
        "tumor": patient_info["tumor"],
        "accuracy": accuracy  # Thêm accuracy vào kết quả
    }
