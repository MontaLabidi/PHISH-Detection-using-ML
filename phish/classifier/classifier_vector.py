from numpy import array
from sklearn.externals import joblib


def classify(list):
    vector = []
    vector.append(list)
    classifier = joblib.load('classifier/classifier.pkl')
    prediction = classifier.predict(array(vector))
    # print ("Predictions on testing data computed.")
    print(prediction)
    return (prediction[0])
