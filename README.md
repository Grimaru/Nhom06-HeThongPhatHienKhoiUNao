#### Our main project for the Big Data subject
#### Main coder: Grimaru
#### Email: rinnenguyenlife4u@gmail.com (sub: 22dh112315@st.huflit.edu.vn)
#### Link dataset: https://www.kaggle.com/datasets/andrewmvd/brain-tumor-segmentation-in-mri-brats-2015
#### I converted the nii file to png to save space on my local machine (I only used the middle slice) (but according to the teacher's comments, our images would lose a lot of features). I made the log files based on an application called Altair AI Studio (formerly called Rapidminer Studio). #### In the data section, I made 6 log files corresponding to:
##### - 3 image log files (according to 3 years: 2018, 2019, 2020 with columns patient ID, flair, seg, t1, t1ce, t2
###### + Those columns will contain the address containing that image)
##### - 3 info log files (according to 3 years: 2018, 2019, 2020 with columns patient ID, Age, Survival, ResectionStatus, Grade, Yes/no tumor)
###### + I made my own code for the Yes/no tumor column. I threw all the png images in for the code to run so it could comment on whether there was a tumor or not. As well as looking at the number of tumors, I also looked at whether it was just "yes" or "no" tumor.
###### + The Grade column has only 2 labels: HGG (High-Grade Glioma) and SGG (Secondary Glioblastoma)
###### + The ResectionStatus column has only 3 labels: GTR (Gross Total Resection), STR (Subtotal Resection) and N/A.
#### Regarding the .py file, I will write the patient's ID for the system to find. After it maps to the patient's ID, if that ID is available, the system will automatically display information about that ID through the log info as well as cross-reference the log image through that ID to show all the images (flair, seg, t1, t1ce, t2) as well as predict the tumor (yes or no) through the use of Active Contours. If Active Contours can isolate the tumor, it means there is a tumor and vice versa, if it displays an image that is only black, it means there is no tumor.
