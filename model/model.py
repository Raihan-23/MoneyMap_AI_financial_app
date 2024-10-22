import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def predict_spending(data):
    if len(data) < 2:
        return None
    
    # Prepare data
    df = pd.DataFrame(data)
    
    # Encoding categorical data (simple example, extend as needed)
    df = pd.get_dummies(df, columns=['category'], drop_first=True)
    
    X = df[['income'] + list(df.columns[df.columns.str.startswith('category_')])]
    y = df['expense']
    
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    
    # Make prediction based on the last income and categories
    last_entry = df.iloc[-1]
    last_input = np.array(last_entry[['income'] + list(df.columns[df.columns.str.startswith('category_')])]).reshape(1, -1)
    
    prediction = model.predict(last_input)
    
    return round(prediction[0], 2)  # Round the prediction for better display
