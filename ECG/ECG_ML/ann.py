import pandas as pd
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
import keras


df=pd.read_csv("features.csv")
y = df["type"].values


X = df[df.columns[2:]].values
X = scale(X)
print(X.shape, y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=123)

print("Number of Normals : {}".format(df[df["type"] == 0].shape[0]))
print("Number of VEBs    : {}".format(df[df["type"] == 1].shape[0]))




# Create your first MLP in Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)
model = Sequential()
model.add(Dense(128, input_dim=8, activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X_train, y_train, epochs=100, batch_size=128)
# evaluate the model
scores = model.evaluate(X_test, y_test)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

