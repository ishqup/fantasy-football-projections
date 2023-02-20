import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler

train_data = pd.read_csv("train.csv", sep=",")

x = np.array(train_data.drop(["Actual","Year","Pos"],axis=1)) # Features
y = np.array(train_data["Actual"]) # Labels

test_data = pd.read_csv("test.csv", sep=",")
x_test = np.array(test_data.drop(["Actual","Year","Pos"],axis=1))

linear = linear_model.LassoCV()

xdel = np.delete(x,0,1)
xdel2 = np.delete(x_test,0,1)

sc = StandardScaler()
sc.fit(xdel)

x_train_std = sc.transform(xdel)
x_test_std = sc.transform(xdel2)

linear.fit(x_train_std,y)
predictions = linear.predict(x_test_std)

column_names = list(test_data.columns)
del column_names[0:4]
reg_coeff = linear.coef_
reg_int = linear.intercept_
column_names = np.append(column_names, "yInt")
reg_coeff = np.append(reg_coeff, reg_int)
var = [column_names,reg_coeff]
coeff = pd.DataFrame(zip(*var), columns=["Variable","Coefficient"])
coeff.to_csv("coeff.csv", index=False)

players = np.array(test_data["Player"])
data = [players,predictions]
predict = pd.DataFrame(zip(*data), columns=["Player","p2023"])
predict.to_csv("predict.csv", index=False)