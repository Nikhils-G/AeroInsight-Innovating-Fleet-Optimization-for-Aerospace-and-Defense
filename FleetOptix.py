import logging
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from flask import Flask, jsonify
import threading
import time

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

class AerospaceAnalyticsPlatform:
    def __init__(self):
        self.scalers_initialized = False
        self.models_initialized = False
        self.scalers = {}
        self.models = {}
        self.init_scalers_and_models()

    def init_scalers_and_models(self):
        if not self.scalers_initialized:
            logging.info("Initializing scalers...")
            # Initialize scalers for each feature (e.g. for different model inputs)
            self.scalers['fuel_efficiency'] = MinMaxScaler()
            self.scalers_initialized = True
        
        if not self.models_initialized:
            logging.info("Initializing models...")
            # Initialize models
            self.models = self.initialize_models()
            self.models_initialized = True

    def initialize_models(self):
        models = {}
        # Load or create models for each target (e.g., fuel efficiency)
        models['fuel_efficiency'] = self.create_lstm_model(10)  # Assuming 10 features for fuel_efficiency
        return models

    def create_lstm_model(self, input_dim):
        model = Sequential()
        
        # Adding Input layer (to avoid Keras warnings)
        model.add(Input(shape=(input_dim, 1)))
        
        # Adding LSTM layers
        model.add(LSTM(50, activation='relu', return_sequences=True))
        model.add(LSTM(50, activation='relu'))
        
        # Dense output layer
        model.add(Dense(1))
        
        # Compile the model
        model.compile(optimizer='adam', loss='mse')
        
        return model

    def train_model(self, model, X_train, y_train, epochs=10, batch_size=32):
        # Train the model
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)

    def evaluate_model(self, model, X_test, y_test):
        # Evaluate the model and return the MSE
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        return mse

    def run_fuel_efficiency_simulation(self):
        # Generate some dummy training data
        X_train = np.random.rand(100, 10, 1)
        y_train = np.random.rand(100, 1)
        
        # Generate some dummy test data
        X_test = np.random.rand(20, 10, 1)
        y_test = np.random.rand(20, 1)
        
        # Scale the data
        X_train_scaled = self.scalers['fuel_efficiency'].fit_transform(X_train.reshape(-1, 10)).reshape(100, 10, 1)
        X_test_scaled = self.scalers['fuel_efficiency'].transform(X_test.reshape(-1, 10)).reshape(20, 10, 1)
        
        # Train the fuel_efficiency model
        self.train_model(self.models['fuel_efficiency'], X_train_scaled, y_train)
        
        # Evaluate the fuel_efficiency model
        mse = self.evaluate_model(self.models['fuel_efficiency'], X_test_scaled, y_test)
        return mse

@app.route('/api/fuel_efficiency')
def get_fuel_efficiency():
    platform = AerospaceAnalyticsPlatform()
    mse = platform.run_fuel_efficiency_simulation()
    return jsonify({'mse': mse})

def run_simulation_thread():
    platform = AerospaceAnalyticsPlatform()
    
    while True:
        # Running the fuel_efficiency simulation
        platform.run_fuel_efficiency_simulation()
        time.sleep(5)  # Simulate a delay

# Main entry point
if __name__ == '__main__':
    # Running the simulation in a separate thread
    simulation_thread = threading.Thread(target=run_simulation_thread)
    simulation_thread.start()
    
    # Start the Flask app
    app.run(debug=True)
