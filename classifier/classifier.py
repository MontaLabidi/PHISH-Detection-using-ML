import numpy as np
import pydotplus
from numpy import genfromtxt
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.externals.six import StringIO
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.tree import export_graphviz


def load_data():
    phish_data = genfromtxt('../data/extracted_Phish.csv', delimiter=',')

    non_phish_data = genfromtxt('../data/extracted_Non_Phish.csv', delimiter=',')
    # phish_data=np.delete(phish_data,11,1)
    # non_phish_data= np.delete(non_phish_data,11,1)

    print(len(phish_data) - len(phish_data[~np.isnan(phish_data).any(axis=1)]))
    print(len(non_phish_data) - len(non_phish_data[~np.isnan(non_phish_data).any(axis=1)]))
    # phish_data=phish_data[~np.isnan(phish_data).any(axis=1)]
    # non_phish_data=non_phish_data[~np.isnan(non_phish_data).any(axis=1)]

    X = np.concatenate((phish_data, non_phish_data), axis=0)

    Y = [1] * len(phish_data) + [0] * len(non_phish_data)

    # Create our imputer to replace missing values with the mean
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp = imp.fit(X)
    X = imp.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=5)
    return X, Y, X_train, y_train, X_test, y_test


if __name__ == '__main__':

    # Load the training data
    X, Y, train_inputs, train_outputs, test_inputs, test_outputs = load_data()
    # print(test_outputs)
    print("Training data loaded.")
    print('training data size : ', len(train_inputs))
    print('testing data size : ', len(test_inputs))

    classifier = RandomForestClassifier(n_estimators=11, random_state=0)
    classifier1 = svm.SVC(kernel='linear')
    classifier2 = tree.DecisionTreeClassifier()
    cl = RandomForestClassifier()
    cl1 = svm.SVC(kernel='linear')
    cl2 = tree.DecisionTreeClassifier()
    print("classifier created.")

    print("Beginning model training.")
    # Train the decision tree classifier
    classifier.fit(train_inputs, train_outputs)
    classifier1.fit(train_inputs, train_outputs)
    classifier2.fit(train_inputs, train_outputs)
    print("Model training completed.")

    # Use the trained classifier to make predictions on the test data
    predictions = classifier.predict(test_inputs)
    predictions1 = classifier1.predict(test_inputs)
    predictions2 = classifier2.predict(test_inputs)
    print("Predictions on testing data computed.")

    # Print the accuracy (percentage of phishing websites correctly predicted)
    accuracy = 100.0 * accuracy_score(test_outputs, predictions)
    accuracy1 = 100.0 * accuracy_score(test_outputs, predictions1)
    accuracy2 = 100.0 * accuracy_score(test_outputs, predictions2)
    print("The accuracy of your decision tree on testing data is: " + str(accuracy))
    print("The accuracy of your decision tree on testing data is: " + str(accuracy1))
    print("The accuracy of your decision tree on testing data is: " + str(accuracy2))

    print("feature importances :")
    # Print feature importances

    for i, feature in enumerate(classifier.feature_importances_):
        print('Feature ', i, ' = ', feature * 100)
    for i, feature in enumerate(classifier2.feature_importances_):
        print('Feature ', i, ' = ', feature * 100)

    joblib.dump(classifier2, 'classifier.pkl')
    print("classifier saved !")
    print(classifier2.feature_importances_)

    score = cross_val_score(cl, X, Y, cv=6)
    score1 = cross_val_score(cl1, train_inputs, train_outputs, cv=6)
    score2 = cross_val_score(cl2, train_inputs, train_outputs, cv=6)
    print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))
    print("Accuracy: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
    print("Accuracy: %0.2f (+/- %0.2f)" % (score2.mean(), score2.std() * 2))

    functions = ['having_IP_Address',
                 'Shortining_Service',
                 'having_At_Symbol',
                 'double_slash_redirecting',
                 'Prefix_Suffix',
                 'having_Sub_Domain',
                 'Domain_registeration_length',
                 'port',
                 'HTTPS_token',
                 'URL_of_Anchor',
                 'Redirect',
                 'Iframe',
                 'age_of_domain',
                 'SFH']
    print(classifier.n_features_)
    print(classifier2.max_features_)
    # Visualisation of the Classifier
    # dot_data = StringIO()
    # export_graphviz(classifier.estimators_[0], out_file=dot_data, feature_names=functions,
    #                 class_names=['Non_Phish', 'Phish'], filled=True, rounded=True, special_characters=True)
    # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    # display(Image(graph.create_png()))
    # graph.write_pdf('kl.pdf')
