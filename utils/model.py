import pickle
import numpy as np

# Load the trained model from a pickle file
def load_model():
    with open("trained_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# Function to predict crop yield using the loaded model
def predict_yield(model, input_data):
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)
    return prediction[0]
