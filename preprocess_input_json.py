import pandas as pd
import warnings

# Ignore all warnings within this block
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

def transform_column(column):
    if column.name == 'x12':
        column = pd.to_numeric(column.astype(str).str.replace('[$,()]', '', regex=True), errors='coerce')

    elif column.name == 'x63':
        column = pd.to_numeric(column.astype(str).str.replace('%', ''), errors='coerce') / 100.0
    return column

def preprocess(df, imputer, std_scaler):
    # 1. Fixing the money and percents
    columns_to_transform = ['x12', 'x63']
    df[columns_to_transform] = df[columns_to_transform].apply(transform_column)

    columns_to_drop = ['x5', 'x31', 'x81', 'x82']
    df_subset = df.drop(columns=columns_to_drop)

    # 2.Use the loaded imputer to transform the validation data
    df_imputed = pd.DataFrame(imputer.transform(df_subset), columns=df_subset.columns)
    # Use the loaded scaler to standardize the features
    df_imputed_std = pd.DataFrame(std_scaler.transform(df_imputed), columns=df_imputed.columns)

    # 3 create dummies
    dumb5 = pd.get_dummies(df['x5'], drop_first=True, prefix='x5', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb5], axis=1, sort=False)

    dumb31 = pd.get_dummies(df['x31'], drop_first=True, prefix='x31', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb31], axis=1, sort=False)

    dumb81 = pd.get_dummies(df['x81'], drop_first=True, prefix='x81', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb81], axis=1, sort=False)

    dumb82 = pd.get_dummies(df['x82'], drop_first=True, prefix='x82', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb82], axis=1, sort=False)

    del dumb5, dumb31, dumb81, dumb82

    return df_imputed_std
