# app.py
# from flask import Flask, request, jsonify, abort
from preprocess_input_json import preprocess
from scipy.special import expit

import pandas as pd
import joblib
import warnings
import os

# Ignore all warnings within this block
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

# Load variables, model weights, scaler, and imputer from the file

def predict(data,model_components):
    """
    data : Data passed in the API
    model_components: model components as a pickel file and other resources from trained model 
    
    """

    variables = model_components['variables']
    print(variables)
    trained_model = model_components['model_weights']

    with open(os.path.join(os.getcwd(),'lib/modelcomponents', model_components['imputer_file']), 'rb') as imputer_file:
        imputer = joblib.load(imputer_file)

    with open(os.path.join(os.getcwd(),'lib/modelcomponents', model_components['scaler_file']), 'rb') as scaler_file:
        std_scaler = joblib.load(scaler_file)

    # Get the raw data from the API request
    raw_data = data.copy()
    print("---------processingtestdata----------")
    # Preprocess the incoming data
    test_imputed_std = preprocess(raw_data,imputer,std_scaler)

    print("----------Making Predictions-----------")
    # Extract linear predicted values for the positive class
    linear_predicted_values = trained_model.predict(test_imputed_std[variables], linear=True)

    # Apply the logistic function to get the probabilities
    predicted_probabilities = expit(linear_predicted_values)

    # Convert probabilities to predicted class (assuming a threshold of 0.5,adjust this threshold)
    predicted_class = (predicted_probabilities >= 0.5).astype(int)

    # Add columns to the DataFrame
    test_imputed_std['probability_positiveclass'] = predicted_probabilities
    unique_variables = list({col.split('_')[0] for col in variables})
    test_imputed_std['predicted_class'] = predicted_class
    
    print("----------combining results-----------")
    # Combine results into a DataFrame
    results_df = pd.DataFrame({

        "probability_positiveclass": predicted_probabilities,
        "selected_features": [unique_variables] * len(predicted_class),  # Repeat variables for each data point
        "predicted_class": predicted_class
    })
    # Convert DataFrame to JSON format
    results_json = results_df.to_json(orient='records')

    # Save JSON to a file
    with open('results.json', 'w') as json_file:
        json_file.write(results_json)

    del test_imputed_std
    del variables
    del trained_model
    del linear_predicted_values
    del predicted_probabilities
    del predicted_class
    del results_df
    del results_json

# Load the model components
with open('lib/modelcomponents/model.pkl', 'rb') as model_file:
    model_components = joblib.load(model_file)

data = pd.read_json('lib/data/test.json')
predict(data,model_components)