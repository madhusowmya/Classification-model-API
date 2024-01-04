# Import necessary libraries
from flask import Flask, request, jsonify
from preprocess_input_json import preprocess 
from scipy.special import expit

import pandas as pd
import joblib
import warnings
import os
import numpy as np 

# Ignore all warnings within this block
with warnings.catch_warnings():
    warnings.simplefilter("ignore")


app = Flask(__name__)

def predict(data, model_components):

    """
    data : Data passed in the API
    model_components: model components as a pickel file and other resources from trained model 
    
    """
    variables = model_components['variables']
    trained_model = model_components['model_weights']

    # Assuming 'imputer.pkl' and 'scaler.pkl' are in the 'lib/modelcomponents' directory
    imputer_path = os.path.join(os.getcwd(), 'lib/modelcomponents', model_components['imputer_file'])
    scaler_path = os.path.join(os.getcwd(), 'lib/modelcomponents', model_components['scaler_file'])

    with open(imputer_path, 'rb') as imputer_file:
        imputer = joblib.load(imputer_file)

    with open(scaler_path, 'rb') as scaler_file:
        std_scaler = joblib.load(scaler_file)

    raw_data = pd.DataFrame(data)  # Convert JSON data to a DataFrame

    # Preprocess the incoming data
    test_imputed_std = preprocess(raw_data, imputer, std_scaler)

    missing_columns = [var for var in variables if var not in test_imputed_std.columns]

    if missing_columns:
        # Reindex the DataFrame with the specified columns, and fill missing columns with NaN
        test_imputed_std = test_imputed_std.reindex(columns=test_imputed_std.columns.union(variables))
        test_imputed_std = test_imputed_std.fillna({col: 0 for col in variables})

    
    linear_predicted_values = trained_model.predict(test_imputed_std[variables], which="linear")

    predicted_probabilities = expit(np.asarray(linear_predicted_values, dtype=np.float64))

    predicted_class = (predicted_probabilities >= 0.5).astype(int)
    
    test_imputed_std['probability_positiveclass'] = predicted_probabilities
    unique_variables = list({col.split('_')[0] for col in variables})
    test_imputed_std['predicted_class'] = predicted_class

    # Combine results into a DataFrame
    results_df = pd.DataFrame({
        "probability_positiveclass": predicted_probabilities,
        "selected_features": [unique_variables] * len(predicted_class),
        "predicted_class": predicted_class
    })

    # Convert DataFrame to JSON format
    results_json = results_df.to_json(orient='records')

    # Return JSON response
    return results_json

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        data = request.get_json()

        # Load the model components
        with open('lib/modelcomponents/model.pkl', 'rb') as model_file:
            model_components = joblib.load(model_file)

        # Perform prediction
        prediction_result = predict(data, model_components)

        return prediction_result

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True,port=1313)