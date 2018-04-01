from sklearn import tree
import numpy as np
import csv
import os
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib



def load_data():
	pwd = os.path.dirname(__file__)
	phish_data = []
	non_phish_data = []
	# Load the training data from the CSV files
	with open(pwd+'/Phish_dataset.csv', newline='') as f:
		reader = csv.reader(f, delimiter=',',quoting=csv.QUOTE_NONE)
		for row in reader:
			phish_data.append(row)

	with open(pwd+'/non_Phish_dataset.csv', newline='') as f:
		reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
		for row in reader:
			non_phish_data.append(row)
			
	X = phish_data+non_phish_data
	y = [1]*len(phish_data) + [0]*len(non_phish_data)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state=5)
	


	# Return the four arrays
	return np.array(X_train), np.array(y_train),np.array( X_test), np.array(y_test)


#def build_classifier(train_inputs, train_outputs):
# Load the training data
train_inputs, train_outputs, test_inputs, test_outputs = load_data()
# Create a decision tree classifier model using scikit-learn
classifier = tree.DecisionTreeClassifier()
print ("Decision tree classifier created.")

#print ("Beginning model training.")
# Train the decision tree classifier
classifier.fit(train_inputs, train_outputs)
#print ("Model training completed.")

joblib.dump(classifier, 'classifier.pkl')
print ("classifier saved !")
"""def get_classifier():
	
	#print(train_inputs[0])

	classifier=build_classifier(train_inputs, train_outputs)
	return classifier"""