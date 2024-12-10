import unittest
from unittest.mock import patch
from data_analysis_app import DataAnalysisApp
import pandas as pd

class TestDataAnalysisApp(unittest.TestCase):
    @patch('requests.get')  # Mocking external requests (like the API call)
    def test_load_api_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'results': [{'profile_id': '123', 'name': 'Test'}]}
        
        app = DataAnalysisApp(root=None)  # Instantiate the app
        app.load_api_data()  # Call the method
        
        # Test that DataFrame is populated with the expected data
        self.assertIsNotNone(app.df)
        self.assertEqual(len(app.df), 1)  # Check that one row was loaded

    def test_clean_data(self):
        app = DataAnalysisApp(root=None)
        app.df = pd.DataFrame({'total_amount_of_payment_usdollars': [100, 0, 5000000, None, 2000]})
        app.clean_data()
        
        # Ensure the DataFrame is cleaned (NaN and outliers removed)
        self.assertEqual(len(app.df), 3)  # 3 rows should remain after cleaning

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_export_results(self, mock_asksaveasfilename):
        mock_asksaveasfilename.return_value = 'test.csv'
        
        app = DataAnalysisApp(root=None)
        app.df = pd.DataFrame({'profile_id': ['123'], 'name': ['Test']})
        
        app.export_results()  # Simulate the export functionality
        
        # Check if the file was created successfully
        self.assertTrue(os.path.exists('test.csv'))  # File should exist after export

if __name__ == "__main__":
    unittest.main()
