import cv2 
from __main__ import app
import numpy as np
import os
import tensorflow as tf
#from tensorflow.keras.models import load_model
#import keras
#from keras.models import model_from_json
#from keras.models import Model
#-----------------------------------------------------------------------------------------------------

#---------------------------------configuracion-------------------------------------------------------
app.config["MODEL_FOLDER"]="static/models/"
#app.config["WEIGHT_FOLDER"]="static/weight/"
#model="Est_Franco_modif_30_ep_IMGS_NEGAT.json"
#weight="Est_Franco_modif_30_ep_IMGS_NEGAT.h5"
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
    new_model = tf.keras.models.load_model(os.path.join(app.config["MODEL_FOLDER"],model))
    
    img = tf.keras.utils.load_img( nombre_archivo, target_size=(img_height, img_width), color_mode="grayscale")
    img_array = tf.keras.utils.img_to_array(img)/255.0
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = new_model.predict(img_array)
    #predictions = np.array([[0.3204914 , 0.4224188 , 0.2368293 , 0.02026045]])

    return predictions       
        