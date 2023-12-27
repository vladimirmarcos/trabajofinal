import cv2 
from . import servicios_bp
import numpy as np
import os
import tensorflow as tf
from flask import current_app
from keras.models import load_model


#-----------------------------------------------------------------------------------------------------

#---------------------------------configuracion-------------------------------------------------------

model="modelo_Kermani_Ver01.h5"
ALLOWED_EXTENSIONS=set(['png',"jpg","jpeg"])
img_height = 256
img_width = 256
#-----------------------------------------------------------------------------------------------------

def allowed_file(file):
    
    file=file.split('.')
    if file[1] in ALLOWED_EXTENSIONS: 
        return True
    return False
     

def red(nombre_archivo):    
    new_model=os.path.join(current_app.config["MODEL_FOLDER"],model)
    
    new_model = tf.keras.models.load_model(os.path.join(current_app.config["MODEL_FOLDER"],model))
    
    
    
    img = tf.keras.utils.load_img( nombre_archivo, target_size=(img_height, img_width), color_mode="grayscale")
    img_array = tf.keras.utils.img_to_array(img)/255.0
    img_array = tf.expand_dims(img_array, 0) 
    predictions = new_model.predict(img_array)
    return list (predictions[0] )  