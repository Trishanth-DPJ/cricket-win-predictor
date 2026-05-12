import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
import joblib
import os
import json

def train_and_evaluate_models():
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'ipl_data.csv')
    df = pd.read_csv(data_path)
    
    # Features and Target
    X = df.drop('result', axis=1)
    y = df['result']
    
    # Identify column types
    categorical_cols = ['batting_team', 'bowling_team', 'city', 'toss_winner', 'toss_decision']
    numerical_cols = ['target_score', 'current_score', 'balls_left', 'wickets_left', 'crr', 'rrr', 'powerplay', 'recent_performance']
    
    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_cols)
        ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Models dictionary
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'K-Nearest Neighbor': KNeighborsClassifier(n_neighbors=5),
        'Neural Network': MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
    }
    
    results = {}
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    print("Training and evaluating models...")
    for name, model in models.items():
        # Create pipeline
        clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        
        # Train
        clf.fit(X_train, y_train)
        
        # Predict
        y_pred = clf.predict(X_test)
        y_proba = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else None
        
        # Evaluate
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        roc_data = {}
        if y_proba is not None:
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            roc_data = {'fpr': fpr.tolist(), 'tpr': tpr.tolist(), 'auc': auc(fpr, tpr)}
        
        results[name] = {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1,
            'Confusion_Matrix': cm,
            'ROC': roc_data
        }
        
        print(f"{name}: Accuracy = {acc:.4f}")
        
        # Check best model
        if acc > best_accuracy:
            best_accuracy = acc
            best_model = clf
            best_model_name = name
            
    print(f"\nBest Model: {best_model_name} with Accuracy = {best_accuracy:.4f}")
    
    # Save best model
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'best_model.pkl')
    joblib.dump(best_model, model_path)
    
    # Save results as JSON
    results_path = os.path.join(os.path.dirname(__file__), 'models', 'evaluation_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"Model saved to {model_path}")
    print(f"Results saved to {results_path}")

if __name__ == "__main__":
    train_and_evaluate_models()
