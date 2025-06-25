import unittest
from unittest.mock import patch, mock_open
from make_request import make_request, take_first_ten, write_to_file


class TestMakeRequest(unittest.TestCase):

    def test_extract_top_n(self):
        data = list(range(15))
        top_10 = take_first_ten(data)
        self.assertEqual(len(top_10), 10)
        self.assertEqual(top_10, list(range(10)))

    def test_extract_less_than_n(self):
        data = list(range(5))
        top = take_first_ten(data)
        self.assertEqual(len(top), 5)
        self.assertEqual(top, list(range(5)))

    @patch("make_request.requests.get")
    def test_fetch_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["a", "b", "c"]
        data = make_request()
        self.assertEqual(data, ["a", "b", "c"])

    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file(self, mock_file):
        test_data = {"foo": "bar"}
        write_to_file(test_data, filename="test_output.json")
        mock_file().write.assert_called()  # or use call_args to check exact JSON content

