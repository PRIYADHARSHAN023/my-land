import joblib

def load_model():
    return joblib.load("trained_model.pkl")

def predict_yield(model, features):
    return model.predict([features])[0]
