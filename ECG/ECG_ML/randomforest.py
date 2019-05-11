import pandas as pd
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
import keras

df=pd.read_csv("./output/features.csv")
y = df["type"].values


X = df[df.columns[2:]].values
X = scale(X)
print(X.shape, y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=123)

print("Number of Normals : {}".format(df[df["type"] == 0].shape[0]))
print("Number of VEBs    : {}".format(df[df["type"] == 1].shape[0]))

from sklearn.metrics import accuracy_score, precision_score, recall_score

def  metrics(y_true, y_pred):
   print("Accuracy  : {}".format(accuracy_score(y_true, y_pred)))
   print("Precision : {}".format(precision_score(y_true, y_pred)))
   print("Recall    : {}".format(recall_score(y_true, y_pred)))






from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, max_depth=2,
                            random_state=0)
rf.fit(X_train, y_train)
y_predict_rf = rf.predict(X_test)
metrics(y_test,y_predict_rf)
