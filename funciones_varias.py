import cv2 
from app import app
import numpy as np
import os
import random
import keras
from keras.models import model_from_json
from keras.models import Model
#-----------------------------------------------------------------------------------------------------

#---------------------------------configuracion-------------------------------------------------------
app.config["MODEL_FOLDER"]="static/models"
app.config["WEIGHT_FOLDER"]="static/weight"
model="Est_Franco_modif_30_ep_IMGS_NEGAT.json"
weight="Est_Franco_modif_30_ep_IMGS_NEGAT.h5"
ALLOWED_EXTENSIONS=set(['png',"jpg","jpeg"])

#-----------------------------------------------------------------------------------------------------


def allowed_file(file):
    
    file=file.split('.')
    if file[1] in ALLOWED_EXTENSIONS: 
        return True
    return False
# Esta función toma un conjunto de imágenes y las convierte en X,Y donde X es la imagen e Y el label
def get_labeled_data(img_entrada):
    i=0
    X=[]
    Y=[]
    img = cv2.imread(img_entrada)
    for image in img_entrada:  
       
        if 'NORMAL' in image:
          if i<100:
            X.append(255-img)
            i=i+1
    
        if 'MH' in image:
          art=1
           
           
          X.append(img-255)
    
        if 'DR' in image:
            
            Y.append([0,1,0])

            X.append(255-img)
    
        if 'CSR8' in image:
             
             Y.append([0,0,1])
            
             X.append(255-img)
          
    
    X.append(255-img)
    Y.append([0,0,1])
      
    return X,Y
def red(nombre_archivo):
            x_ex_temp,y_ex_temp=get_labeled_data(nombre_archivo)
            X_extrap=np.array(x_ex_temp)
            Y_extrap=np.array(y_ex_temp)
            X_extrap = X_extrap.astype('float32')
            X_extrap/=255.0
            json_file = open(os.path.join(app.config["MODEL_FOLDER"],model), 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            cnn = model_from_json(loaded_model_json)
            weights_path=os.path.join(app.config["WEIGHT_FOLDER"],weight)
            cnn.load_weights(weights_path)
            cnn.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
            cnn.summary()
            i=random.randint(0, (len(X_extrap)-1))
            imagen_a_pred=X_extrap[i]
            A=imagen_a_pred[np.newaxis,:, : ]
            predictions_raw= cnn.predict(A);
            predictions=np.argmax(predictions_raw, axis=1)  #transformo las predicciones en enteros
            y_pred = predictions; 
            y_true=Y_extrap[i] 
            y_true=np.argmax(y_true, axis=0)
           # print("El label real es:    ",labels[y_true])
            #print("El label predicho es:",labels[y_pred[0]])
            predictions=np.argmax(predictions_raw, axis=1)  #transformo las predicciones en enteros
            y_pred = predictions; 
            y_true=Y_extrap[i] #valor real
            y_true=np.argmax(y_true, axis=0)
            return predictions_raw