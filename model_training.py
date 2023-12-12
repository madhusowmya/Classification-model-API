from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import pandas as pd
import numpy as np
import joblib

class Model:
    def __init__(self):
        pass

    def preprocess_input(self, data):
        train_val = data.copy(deep=True)

        # Fixing the money and percents
        train_val['x12'] = train_val['x12'].str.replace('$', '')
        train_val['x12'] = train_val['x12'].str.replace(',', '')
        train_val['x12'] = train_val['x12'].str.replace(')', '')
        train_val['x12'] = train_val['x12'].str.replace('(', '-')
        train_val['x12'] = train_val['x12'].astype(float)
        train_val['x63'] = train_val['x63'].str.replace('%', '')
        train_val['x63'] = train_val['x63'].astype(float)

        # Creating the train/val/test set
        x_train, x_val, y_train, y_val = train_test_split(train_val.drop(columns=['y']), train_val['y'],
                                                          test_size=0.1, random_state=13)
        x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=4000, random_state=13)

        # Smashing sets back together
        train = pd.concat([x_train, y_train], axis=1, sort=False).reset_index(drop=True)

        # With mean imputation from Train set
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        train_imputed = pd.DataFrame(imputer.fit_transform(
            train.drop(columns=['y', 'x5', 'x31', 'x81', 'x82'])), columns=train.drop(columns=['y', 'x5', 'x31', 'x81', 'x82']).columns)
        std_scaler = StandardScaler()
        train_imputed_std = pd.DataFrame(std_scaler.fit_transform(train_imputed), columns=train_imputed.columns)

        # Create dummies
        dumb5 = pd.get_dummies(train['x5'], drop_first=True, prefix='x5', prefix_sep='_', dummy_na=True)
        train_imputed_std = pd.concat([train_imputed_std, dumb5], axis=1, sort=False)

        dumb31 = pd.get_dummies(train['x31'], drop_first=True, prefix='x31', prefix_sep='_', dummy_na=True)
        train_imputed_std = pd.concat([train_imputed_std, dumb31], axis=1, sort=False)

        dumb81 = pd.get_dummies(train['x81'], drop_first=True, prefix='x81', prefix_sep='_', dummy_na=True)
        train_imputed_std = pd.concat([train_imputed_std, dumb81], axis=1, sort=False)

        dumb82 = pd.get_dummies(train['x82'], drop_first=True, prefix='x82', prefix_sep='_', dummy_na=True)
        train_imputed_std = pd.concat([train_imputed_std, dumb82], axis=1, sort=False)
        train_imputed_std = pd.concat([train_imputed_std, train['y']], axis=1, sort=False)

        del dumb5, dumb31, dumb81, dumb82

        return train_imputed_std, imputer, std_scaler

    def feature_selection(self, df):
        exploratory_LR = LogisticRegression(penalty='l1', fit_intercept=False, solver='liblinear')
        exploratory_LR.fit(df.drop(columns=['y']), df['y'])
        exploratory_results = pd.DataFrame(df.drop(columns=['y']).columns).rename(columns={0: 'name'})
        exploratory_results['coefs'] = exploratory_LR.coef_[0]
        exploratory_results['coefs_squared'] = exploratory_results['coefs']**2
        var_reduced = exploratory_results.nlargest(25, 'coefs_squared')
        variables = var_reduced['name'].to_list()

        return variables

    def model_training(self, variables, df):
        logit = sm.Logit(df['y'], df[variables])
        result = logit.fit()
        return result

    def save_model_components(self, variables, trained_model, std_scaler, imputer):
        # Save variables, model weights, scaler, and imputer
        with open('model_components/model.pkl', 'wb') as model_file:
            model_components = {
                'variables': variables,
                'model_weights': trained_model.params,
                'scaler': std_scaler,
                'imputer': imputer
            }
            joblib.dump(model_components, model_file)

    def main(self, raw_data):
        data = pd.read_csv(raw_data)
        data_processed, imputer, scaler = self.preprocess_input(data)
        features = self.feature_selection(data_processed)
        trained_model = self.model_training(features, data_processed)
        self.save_model_components(features, trained_model, scaler, imputer)

# Instantiate the model
my_model = Model()

# Example usage with a raw data file
data_file = 'path_to_your_data.csv'
my_model.main(data_file)
