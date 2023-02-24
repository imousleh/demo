import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Load the preprocessed image data and labels
data = np.load('preprocessed_data.npy')
labels = np.load('labels.npy')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Initialize the SVM classifier
svm = SVC(kernel='linear')

# Train the SVM classifier on the training data
svm.fit(X_train, y_train)

# Use the SVM classifier to predict the labels for the testing data
y_pred = svm.predict(X_test)

# Calculate the accuracy of the classifier on the testing data
accuracy = np.mean(y_pred == y_test)

print('Accuracy:', accuracy)
