import pickle
import pandas as pd

from smolagents import tool
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Function to get the same vectorizer that was used to train the model
def get_vectorizer() -> TfidfVectorizer:
    cleaned_data_path = Path(__file__).resolve().parents[2] / "data" / "twcs_filtered_labeled_1_cleaned.csv"

    df = pd.read_csv(cleaned_data_path)
    X = df['text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(X_train)

    return vectorizer

@tool
def run_model_prediction_pipeline(msg: str) -> str:
    """Predicts the category that the given customer inquiry belongs to.

    Args:
        msg: the incoming customer inquiry, cleaned.

    Returns:
        The model's prediction (i.e., which category the customer's inquiry belongs to).
    
    """
    vectorizer = get_vectorizer()
    text = vectorizer.transform([msg])

    pkl_model_path = Path(__file__).resolve().parents[2] / "models" / "lr_model.pkl"

    model = pickle.load(open(pkl_model_path, "rb"))

    category = model.predict(text)
    return category
