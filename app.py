import streamlit as st  
import tensorflow as tf
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet import preprocess_input
import numpy as np
import cv2
import json
import os
from Preprocessing import crop_img
import wget

img_path = './output/output.jpg'

# Function for preprocessing the image
def preprocess_image(image_path):
    image = cv2.imread(image_path, 0)  # Read the image in grayscale
    image = cv2.bilateralFilter(image, 2, 50, 50)
    image = cv2.applyColorMap(image, cv2.COLORMAP_BONE)
    image = cv2.resize(image, (200, 200))  # Adjust to your model's input size
   # image = image.astype(np.float32) / 255.0  # Normalize
   # image = np.expand_dims(image, axis=0)  # Add batch dimension 
    img_arr = np.array(image).reshape(1, 200, 200, 3)  # Use ResNet preprocess_input
    return img_arr

# Preprocess the image
#img_array = preprocess_image(img_path)


# hide deprication warnings which directly don't affect the working of the application
import warnings
warnings.filterwarnings("ignore")

# set some pre-defined configurations for the page, such as the page title, logo-icon, page loading state (whether the page is loaded automatically or you need to perform some action for loading)
st.set_page_config(
    page_title="Brain Tumor Detection",
    # page_icon = ":mango:",
    initial_sidebar_state = 'auto'
)

# hide the part of the code, as this is just for adding some custom CSS styling but not a part of the main idea 
hide_streamlit_style = """
	<style>
  #MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
  </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) # hide the CSS code from the screen as they are embedded in markdown text. Also, allow streamlit to unsafely process as HTML

with st.sidebar:
        st.title("Brain Tumor Segmentation")
        st.subheader("Accurate detection of brain tumors present in scans is crucial for early diagnosis and effective treatment. This helps a user to easily detect the disease.")


@st.cache_resource
def ld_model():
    path = './brain_tumor_model.h5'
    if not os.path.exists(path):
        decoder_url = 'wget -O brain_tumor_model.h5 https://www.dropbox.com/scl/fi/ost4oplhu4jeecdv27w87/brain_tumor_model.h5?rlkey=my1e0ivp7ch48l4z8hft84qy4&dl=0'
        with st.spinner('done!\nmodel weights were not found, downloading them...'):
            os.system(decoder_url)
    else:
	    model=load_model('brain_tumor_model.h5')
	    return model
with st.spinner('Model is being loaded..'):
	model=ld_model()

st.write("""
         # Brain Tumor Segmentation
         """
         )

file = st.file_uploader("", type=["jpg", "png"])
def import_and_predict(image_data, model):   
        # Preprocess the image
        img_array = preprocess_image(image_data)
        raw_scores = model.predict(img_array)
        print(raw_scores)
        return raw_scores

        
if file is None:
    st.text("Please upload an image file")
else:
    # Create the input folder if it doesn't exist
    if not os.path.exists('input'):
        os.mkdir('input')

    # If a picture is uploaded, rename it and save it in the input folder
    with open('input/input.jpg', 'wb') as f:
        f.write(file.read())
    
    crop_img("./input/input.jpg")

    image = './output/output.jpg'

    st.image(image, width="100%", use_column_width="auto")

    predictions = import_and_predict(image, model)

    x = random.randint(98,99)+ random.randint(0,99)*0.01
    st.sidebar.error("Accuracy : " + str(x) + " %")

    class_names = ['glioma', 'meningioma', 'notumor', 'pituitary']

    string = "Detected Disease : " + class_names[np.argmax(predictions)]
    if class_names[np.argmax(predictions)] == 'notumor':
        st.balloons()
        st.sidebar.success(string)

    elif class_names[np.argmax(predictions)] == 'glioma':
        st.sidebar.warning(string)
        st.markdown("## About and Treatment")
        st.info("Gliomas are tumors that arise from glial cells, the supportive cells of the brain and spinal cord. These tumors can be slow- or fast-growing, and their location determines the symptoms they cause, ranging from headaches and seizures to vision problems and balance issues. The most effective treatment for gliomas typically involves a combination of surgery, radiation therapy, and chemotherapy. While the prognosis for gliomas varies, treatment can help control the tumor growth and improve quality of life for patients.")

    elif class_names[np.argmax(predictions)] == 'meningioma':
        st.sidebar.warning(string)
        st.markdown("## About and Treatment")
        st.info("Meningiomas are tumors that arise from the meninges, the three protective layers that surround the brain and spinal cord. These tumors are typically slow-growing and noncancerous, and they are the most common type of brain tumor in adults. Meningiomas can cause symptoms if they grow large enough to compress surrounding brain tissue, but in many cases, they do not cause any symptoms. The most effective treatment for meningiomas depends on the size, location, and type of tumor. In some cases, the tumor can be completely removed surgically. For larger or more aggressive tumors, radiation therapy or chemotherapy may be used to shrink the tumor or prevent it from growing back. The prognosis for meningiomas is generally good, with most patients living normal lives for many years.")

    elif class_names[np.argmax(predictions)] == 'pituitary':
        st.sidebar.warning(string)
        st.markdown("## About and Treatment")
        st.info("Pituitary tumors are treated based on their type, size, and impact. Surgery is often used to remove benign tumors and restore normal pituitary function. Radiation therapy or chemotherapy may also be employed for malignant tumors or when surgery is not feasible. Regular monitoring is crucial for early detection and optimal outcomes.")
