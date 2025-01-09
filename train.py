import glob
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import json


# define functions
def main():
    # Load configuration from config.json
    config = load_config()

    # Enable autologging
    mlflow.autolog()

    df = get_csvs_df(config['training_data'])
    X_train, X_test, y_train, y_test = split_data(df)
    model = train_model(config['reg_rate'], X_train, X_test, y_train, y_test)

    evaluate_model(model, X_test, y_test)


def load_config():
    """Load configuration from the JSON file."""
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


def get_csvs_df(path):
    """Read and concatenate all CSV files in the given path."""
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


def split_data(df):
    """Split data into training and testing datasets."""
    X = df[['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure', 
            'TricepsThickness', 'SerumInsulin', 'BMI', 
            'DiabetesPedigree', 'Age']].values
    y = df['Diabetic'].values
    return train_test_split(X, y, test_size=0.30, random_state=0)


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    """Train a logistic regression model."""
    model = LogisticRegression(C=1/reg_rate, solver="liblinear") \
        .fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate the model and log metrics."""
    y_hat = model.predict(X_test)
    acc = accuracy_score(y_test, y_hat)
    y_scores = model.predict_proba(X_test)
    auc = roc_auc_score(y_test, y_scores[:, 1])

    print(f"Accuracy: {acc}")
    print(f"AUC: {auc}")

    # Plot ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_scores[:, 1])
    plt.figure(figsize=(6, 4))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.savefig("roc_curve.png")
    print("ROC curve saved as 'roc_curve.png'")


# run script
if __name__ == "__main__":
    # Add space in logs
    print("\n\n")
    print("*" * 60)

    # Run main function
    main()

    # Add space in logs
    print("*" * 60)
    print("\n\n")
