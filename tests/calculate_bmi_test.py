import unittest
from unittest.mock import MagicMock, patch, mock_open
import multiprocessing

mock_bmi_result = [
                    {'Gender': 'Male', 'HeightCm': 171, 'WeightKg': 96, 'bmi': 56.1,
                    'category': 'Very severely obese', 'health_risk': 'Very high risk'}
                ]
mock_category_count = {0: 0, 18.5: 0, 25: 0, 30: 0, 35: 0, 40: 0}

class PoolTest:
    def apply(fun, *args, **kwargs):
        return [mock_bmi_result, {0: 0, 18.5: 0, 25: 0, 30: 0, 35: 0, 40: 1}]

class CalculateBMITest(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"Gender": "Male","HeightCm": 171,"WeightKg": 96}]')
    @patch.object(multiprocessing, "Pool", PoolTest)
    def test_bmi_calculation(self, mock_file):
        from calculator.calculate_bmi import bmi_calculation
        res = bmi_calculation()
        assert open("data/weight_height_data.json").read() == '[{"Gender": "Male","HeightCm": 171,"WeightKg": 96}]'
        mock_file.assert_called_with("data/weight_height_data.json")
        self.assertEqual(res['bmi_with_category'], mock_bmi_result)
        test_bmi_category_count = {
            'underweight_people': 0,
            'normal_weight_people': 0,
            'overweight_people': 0,
            'moderately_obese_people': 0,
            'severely_obese_people': 0,
            'very_severely_obese_people': 1
        }
        self.assertEqual(res['category_wise_count'], test_bmi_category_count)

    def test_calculate_functionality(self):
        test_data = [
            {"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },
            { "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },
            { "Gender": "Male", "HeightCm": 180, "WeightKg": 43 },
            { "Gender": "Female", "HeightCm": 166, "WeightKg": 62}
        ]
        from calculator.calculate_bmi import _calculate
        res = _calculate(list(mock_category_count.keys()), mock_category_count, test_data)
        self.assertEqual(res[0], [{'Gender': 'Male', 'HeightCm': 171, 'WeightKg': 96, 'bmi': 56.1, 'category': 'Very severely obese', 'health_risk': 'Very high risk'}, 
            {'Gender': 'Male', 'HeightCm': 161, 'WeightKg': 85, 'bmi': 52.8, 'category': 'Very severely obese', 'health_risk': 'Very high risk'},
            {'Gender': 'Male', 'HeightCm': 180, 'WeightKg': 43, 'bmi': 23.9, 'category': 'Normal weight', 'health_risk': 'Low risk'},
            {'Gender': 'Female', 'HeightCm': 166, 'WeightKg': 62, 'bmi': 37.3, 'category': 'Severely obese', 'health_risk': 'High risk'}])
        self.assertEqual(res[1], {0: 0, 18.5: 1, 25: 0, 30: 0, 35: 1, 40: 2})
