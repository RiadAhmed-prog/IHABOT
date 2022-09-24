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

score_names=["Normal","Mild","Severe","Critical"]
with open('scalar.pkl','rb') as f:
    scalar= pickle.load(f)
    f.close()


with open('health_model.pkl','rb') as f:
    model= pickle.load(f)
    f.close()


inp=np.array([[98.1,75.0,16.0,140.0,80.0,96.0]])
inp= pd.DataFrame(inp)
inp_x = scalar.transform(inp)

pred= model.predict(inp_x)
print(score_names[pred[0]])