
import unittest
import json
from gpt_api import app, make_suggestions_with_ml, create_model
import numpy as np

class EcuTunerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test the /tune endpoint with mock data
    def test_tune_endpoint(self):
        data = {
            'ecu_type': 'obd2',
            'air_fuel_ratio': 13.5,
            'boost_pressure': 10.5,
            'throttle_position': 75
        }
        response = self.app.post('/tune', data=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('suggestion', response_data)

    # Test the /train endpoint with mock data
    def test_train_endpoint(self):
        data = {
            'ecu_data': {
                'air_fuel_ratio': 14.5,
                'boost_pressure': 9.0,
                'throttle_position': 70
            },
            'tuning_decisions': {
                'throttle_position': 72
            }
        }
        response = self.app.post('/train', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')

    # Test the TensorFlow model prediction functionality
    def test_model_prediction(self):
        model = create_model()
        input_data = np.array([[13.5, 10.5, 75]])  # Mock data
        prediction = model.predict(input_data)
        self.assertEqual(prediction.shape, (1, 1))

if __name__ == '__main__':
    unittest.main()
