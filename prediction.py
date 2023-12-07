import pickle
import pandas as pd

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path)

p = parser.parse_args()
print(p.file_path)


filename = "model/model.pickle"

# load model
loaded_model = pickle.load(open(filename, "rb")) 

# Load the test dataset, in the deployement setting, we will received transaction information in json format 

df = pd.read_csv(p.file_path)


y_test = df['Class']
test_data =  df.drop(columns=['Class'],axis=1)

y_pred_test = loaded_model.predict(test_data)
l = ["fraudulent" if i == 1 else "legitimate" for i in y_pred_test]

pd.DataFrame({'output':l}).to_csv('output/predict.csv', index=False)

print(l[:5]) # in the deployement setting, we will return the result in json format.  



