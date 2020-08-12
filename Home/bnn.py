import vega_datasets as vd
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn import linear_model
import sklearn.metrics as sm

x1 = 0
x2 = 0
x3 = 0

def regresi(x1,x2,x3):
    cr  = vd.data.cars()
    cr['Miles_per_Gallon'] = cr['Miles_per_Gallon'].fillna(cr['Miles_per_Gallon'].mean())
    cr['Horsepower'] = cr['Horsepower'].fillna(cr['Horsepower'].mean())
    print(cr)
    lin_reg = linear_model.LinearRegression()
    lin_reg.fit(cr[['Displacement','Horsepower','Weight_in_lbs']],cr['Miles_per_Gallon'])
    hasil = lin_reg.predict([[x1,x2,x3]])
    return hasil