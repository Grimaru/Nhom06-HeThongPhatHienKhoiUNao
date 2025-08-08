from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.appName("MRI_Tumor_App").getOrCreate()

def load_patient_info():
    # Đọc dữ liệu từ CSV
    df_2018 = spark.read.csv("data/log_info_2018.csv", header=True, inferSchema=True)
    df_2019 = spark.read.csv("data/log_info_2019.csv", header=True, inferSchema=True)
    df_2020 = spark.read.csv("data/log_info_2020.csv", header=True, inferSchema=True)

    # Chỉ giữ lại các cột cần thiết, với ID và Survival tương ứng từng năm
    df_2018 = df_2018.select(
        col("BraTS18ID").alias("BraTS_ID"),
        "Age",
        "Survival",
        "ResectionStatus",
        "Grade",
        col("Yes/no tumor").alias("Tumor")
    ).withColumn("Year", lit(2018))

    df_2019 = df_2019.select(
        col("BraTS19ID").alias("BraTS_ID"),
        "Age",
        "Survival",
        "ResectionStatus",
        "Grade",
        col("Yes/no tumor").alias("Tumor")
    ).withColumn("Year", lit(2019))

    df_2020 = df_2020.select(
        col("BraTS_2020_subject_ID").alias("BraTS_ID"),
        "Age",
        col("Survival_days").alias("Survival"),  # Đổi Survival_days thành Survival
        col("Extent_of_Resection").alias("ResectionStatus"),  # Đổi cho giống ResectionStatus
        "Grade",
        col("Yes/no tumor").alias("Tumor")
    ).withColumn("Year", lit(2020))

    # Union lại
    df = df_2018.unionByName(df_2019).unionByName(df_2020)

    return df

def load_patient_images():
    # Đọc dữ liệu từ CSV
    df_img_2018 = spark.read.csv("data/log_image_2018.csv", header=True, inferSchema=True)
    df_img_2019 = spark.read.csv("data/log_image_2019.csv", header=True, inferSchema=True)
    df_img_2020 = spark.read.csv("data/log_image_2020.csv", header=True, inferSchema=True)

    # Chỉ giữ lại các cột cần thiết
    df_img_2018 = df_img_2018.select(
        col("BraTS18ID").alias("BraTS_ID"),
        "flair", "seg", "t1", "t1ce", "t2"
    ).withColumn("Year", lit(2018))

    df_img_2019 = df_img_2019.select(
        col("BraTS19ID").alias("BraTS_ID"),
        "flair", "seg", "t1", "t1ce", "t2"
    ).withColumn("Year", lit(2019))

    df_img_2020 = df_img_2020.select(
        col("BraTS20ID").alias("BraTS_ID"),
        "flair", "seg", "t1", "t1ce", "t2"
    ).withColumn("Year", lit(2020))

    # Union lại
    df_images = df_img_2018.unionByName(df_img_2019).unionByName(df_img_2020)
    return df_images

def get_patient_info(patient_id):
    df_info = load_patient_info()
    df_images = load_patient_images()

    # Kết hợp dữ liệu theo BraTS_ID
    df = df_info.join(df_images, on="BraTS_ID", how="left")

    # Lọc dữ liệu theo ID bệnh nhân
    patient_df = df.filter(df.BraTS_ID == patient_id).collect()
    
    if not patient_df:
        return None  # Không tìm thấy bệnh nhân
    
    patient = patient_df[0]  # Lấy dòng đầu tiên nếu có nhiều kết quả

    return {
        "id": patient.BraTS_ID,
        "age": patient.Age,
        "status": patient.ResectionStatus,
        "survival": patient.Survival,
        "grade": patient.Grade,
        "tumor": patient.Tumor,
        "flair": patient.flair,
        "seg": patient.seg,
        "t1": patient.t1,
        "t1ce": patient.t1ce,
        "t2": patient.t2
    }

def get_patient_list(grade=None, tumor=None):
    # Trả về danh sách bệnh nhân theo cấp độ (grade) hoặc số lượng khối u (tumor).
    df = load_patient_info()
    if grade:
        df = df.filter(df.Grade == grade)
    if tumor:
        df = df.filter(df.Tumor == tumor)
    return df.collect()