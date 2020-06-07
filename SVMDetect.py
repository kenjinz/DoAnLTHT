import numpy as np
import os
from pathlib import Path
import random
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn.metrics import accuracy_score
import itertools
import joblib
from keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import cv2
from collections import Counter
cap = cv2.VideoCapture(0)
model = VGG16(weights = 'imagenet', include_top = False)
#from SVMClassification import drawImg
labels_index = []
svm_classifier = joblib.load('model_name.npy')
average_proba = []
def predict(test_data):
    ypred_sklearn = svm_classifier.predict_proba(test_data)
    #ypred_sklearn1 = svm_classifier.predict(test_data)
    i=0
    for row in ypred_sklearn:
        print("Row " + str(i+1))
        max_proba = np.amax(row)
        average_proba.append(max_proba)
        if max_proba > 0.75:
            index = np.argmax(row)
            labels_index.append(index)
        else:
            labels_index.append(-1)
        #print(np.amax(row))
        i+=1
        #print(labels_index)
    label = dict(Counter(labels_index))
    # Find Max Value of key of Dictionary:
    max_value = max(label.values())  # maximum value
    max_keys = [k for k, v in label.items() if v == max_value][0]  # getting all keys containing the `maximum`
    result =[]
    # SHOW AVERAGE ACCURACY OF ALGORITHM:
    if max_keys == -1:
        result.append(-1)
        return result # UNDEFINED
    else:
        average_proba_num = sum(average_proba)/len(average_proba)
        accuracy = max_value / 10
        print(accuracy)
        if accuracy > 0.7:
            result.append(max_keys,average_proba_num)
            return result
    # SHOW AVERAGE PROBABILITY OF ALGORITHM:

    #print(max_keys[0])
    return
def detect():
    p2 = Path("TestSet2/")
    test_data = []
    # Prepare Test(Valid) Data
    for test_path in p2.glob("*.jpg"):
        test = image.load_img(test_path, target_size=(224, 224))
        test_array = image.img_to_array(test)
        # Add another Dimension for array
        test_array = np.expand_dims(test_array, axis=0)
        test_array = preprocess_input(test_array)
        # Add feature to img
        vgg16_feature_test = model.predict(test_array)
        test_data.append(vgg16_feature_test)

    test_data = np.array(test_data)
    print(test_data.shape)

    test_data = np.array(test_data, dtype='float32')/255.0

    N = test_data.shape[0]
    test_data = test_data.reshape(N,-1)



    print(predict(test_data))








    #print(ypred_sklearn)
    #print("Do chinh xac cua thuat toan: ")
    #acc = accuracy_score(result_test, ypred_sklearn)
    #print(str(acc * 100) + '%')

    #for i in range(8):
    # if ypred_sklearn[0] == 1:
    #     class_name = "Card"
    # if ypred_sklearn[0] == 0:
    #     class_name = "Chia khoa"
    # if ypred_sklearn[0] == 2:
    #     class_name = "Moc khoa"
    # if ypred_sklearn[0] == 3:
    #     class_name = "LED"

    #print(class_name)
    #return ypred_sklearn


if __name__ == '__main__':
    #print(detect())
    #n = 0

    while True:
        ret,frame = cap.read()
        cv2.imshow('abc', frame)
        n=0
        if cv2.waitKey(1) & 0xFF == ord('y'):
            while(n<10):
                n+=1
                dim = (1280, 960)
                frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

                cv2.imwrite('TestSet2/{:02}.jpg'.format(n), frame)
                print (n)
                #cv2.imwrite('TestSet2/1.jpg', frame)
                #print(detect())
            # detect_result.append(detect())
            # acc = accuracy_score(result_test, detect_result)
            # print(str(acc * 100) + '%')
            cv2.destroyAllWindows()
            break
    detect()
    cap.release()

