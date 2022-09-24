import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report,f1_score,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import pickle

fig_X = 10
fig_y = 8
bins = 25
title_size = 20
color = 'b'
score_names=["Normal","Mild","Severe","Critical"]

score_df = pd.read_csv('/home/portia/riad/Patient Severity Score for Electronic Health Records.csv')
print(score_df.head())

score_df = score_df.rename(columns={'SCORE ':'SCORE'})

X = score_df.drop('SCORE',axis=1)
y = score_df.SCORE

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=11)

scalar = StandardScaler()
X_train = scalar.fit_transform(X_train)
X_test = scalar.transform(X_test)
with open('scalar.pkl','wb') as f:
    pickle.dump(scalar,f)

model= RandomForestClassifier()
model.fit(X_train,y_train)
print(f"Accuracy Score for RandomForestClassifier is : ",model.score(X_test,y_test)*100,"%")


with open('health_model.pkl','wb') as f:
    pickle.dump(model,f)