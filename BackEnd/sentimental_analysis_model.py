import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle

# Load Dataset
def load_data(file_path):
    data = pd.read_csv(file_path)
    if 'Query' not in data.columns or 'mental_health_state' not in data.columns:
        raise ValueError("CSV file must contain 'Query' and 'mental_health_state' columns.")
    return data

# Preprocess and Split Data
def preprocess_data(data):
    X = data['Query']
    y = data['mental_health_state']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Train Model
def train_model(X_train, y_train):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    model = LogisticRegression()
    model.fit(X_train_tfidf, y_train)
    
    return model, vectorizer

# Evaluate Model
def evaluate_model(model, vectorizer, X_test, y_test):
    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_tfidf)
    
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

# Save Model and Vectorizer
def save_model(model, vectorizer, model_path="mental_health_model.pkl", vectorizer_path="vectorizer.pkl"):
    with open(model_path, 'wb') as model_file:
        pickle.dump(model, model_file)
    with open(vectorizer_path, 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

# Load Model and Vectorizer
def load_model(model_path="mental_health_model.pkl", vectorizer_path="vectorizer.pkl"):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

# Predict Mental Health State
def predict(query, model, vectorizer):
    query_tfidf = vectorizer.transform([query])
    prediction = model.predict(query_tfidf)
    return prediction[0]

# Main Execution
if __name__ == "__main__":
    # Replace 'dataset.csv' with your actual dataset file
    file_path = "dataset.csv"
    
    try:
        data = load_data("./dataSets/mental_health_conditions.csv")
        X_train, X_test, y_train, y_test = preprocess_data(data)
        
        model, vectorizer = train_model(X_train, y_train)
        evaluate_model(model, vectorizer, X_test, y_test)
        
        save_model(model, vectorizer)
        print("Model and vectorizer saved successfully.")
        
        # Example query
        model, vectorizer = load_model()
        query = "I feel very anxious and worried all the time."
        prediction = predict(query, model, vectorizer)
        print(f"Predicted Mental Health State: {prediction}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
