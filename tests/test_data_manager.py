import unittest
import pandas as pd
from data.data_manager import DataManager

class TestDataManager(unittest.TestCase):
    
    def setUp(self):
        self.data_manager = DataManager(raw_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/raw' , processed_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/processed')
    #test the row if are working well and present
    def test_load_raw_data_success(self):
        # Assuming BTCUSD_1m.csv exists and is valid
        df = self.data_manager.load_raw_data('BTCUSD', 'BTCUSDT_1m.csv')
        self.assertFalse(df.empty)
        self.assertIn('timestamp', df.columns)
    
    def test_load_raw_data_file_not_found(self):
        df = self.data_manager.load_raw_data('BTCUSD', 'non_existent.csv')
        self.assertTrue(df.empty)
    
    def test_preprocess_data_empty(self):
        df = pd.DataFrame()
        processed_df = self.data_manager.preprocess_data(df)
        self.assertTrue(processed_df.empty)
    
    def test_preprocess_data_valid(self):
        data = {
            'timestamp': ['2020-08-31 21:00:00', '2020-08-31 21:01:00'],
            'Open': [11672.8, 11667.41],
            'High': [11672.86, 11668.0],
            'Low': [11667.37, 11658.44],
            'Close': [11667.41, 11659.45],
            'Volume': [31.158083, 34.03299],
            'support': [11667.41, 11659.45],
            'resistance': [11667.41, 11667.41]
        }
        df = pd.DataFrame(data)
        processed_df = self.data_manager.preprocess_data(df)
        self.assertFalse(processed_df.empty)
        self.assertEqual(processed_df.shape[0], 2)
    
    def test_resample_data_valid(self):
        data = {
            'timestamp': pd.date_range(start='2020-08-31 21:00:00', periods=60, freq='T'),
            'Open': [11672.8]*60,
            'High': [11680.0]*60,
            'Low': [11660.0]*60,
            'Close': [11670.0]*60,
            'Volume': [30.0]*60,
            'support': [11660.0]*60,
            'resistance': [11680.0]*60
        }
        df = pd.DataFrame(data)
        resampled_df = self.data_manager.resample_data(df, '5T')
        self.assertFalse(resampled_df.empty)
        self.assertEqual(resampled_df.shape[0], 12)  # 60 minutes / 5 = 12
        self.assertIn('support', resampled_df.columns)
        self.assertIn('resistance', resampled_df.columns)
    
    def test_resample_data_empty(self):
        df = pd.DataFrame()
        resampled_df = self.data_manager.resample_data(df, '5T')
        self.assertTrue(resampled_df.empty)

if __name__ == '__main__':
    unittest.main()
    
#script to run it python -m unittest tests/test_data_manager.py

