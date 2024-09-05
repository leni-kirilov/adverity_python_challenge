import os
import os.path
import unittest

import petl

from core.services import datasets

TRANSFORMED_CSV_FILENAME = "core/tests/test_data_transformed.csv"
RAW_CSV_FILENAME = "core/tests/test_data_raw.csv"


class DatasetTestCase(unittest.TestCase):

    def tearDown(self):
        # Clean up created files
        for file in os.listdir("."):
            if file.startswith(datasets.CSV_FILENAME_PREFIX):
                os.remove(file)

    def test_get_data_up_to_page_negative(self):
        self.assertRaises(ValueError, datasets.get_data_up_to_page, None, 0)
        self.assertRaises(ValueError, datasets.get_data_up_to_page, "", 0)
        self.assertRaises(ValueError, datasets.get_data_up_to_page, "file-name", -1)

    def test_get_data_up_to_page_1_page(self):
        result = datasets.get_data_up_to_page(TRANSFORMED_CSV_FILENAME, 0)
        self.assertEqual(datasets.PAGE_SIZE, len(result))

        first_item = result[0]
        self.assertEqual("Luke Skywalker", first_item["name"])

    def test_get_data_up_to_page_multiple_pages(self):
        result = datasets.get_data_up_to_page(TRANSFORMED_CSV_FILENAME, 1)
        self.assertEqual(12, len(result))

    def test_get_data_up_to_page_too_many_pages(self):
        result = datasets.get_data_up_to_page(TRANSFORMED_CSV_FILENAME, 10)
        self.assertEqual(12, len(result))

    def test_transform_negative(self):
        self.assertRaises(ValueError, datasets.transform_and_write_to_file, None)
        self.assertRaises(ValueError, datasets.transform_and_write_to_file, {})

    def test_transform(self):
        # GIVEN test data loaded
        test_dict = petl.fromcsv(RAW_CSV_FILENAME).dicts().list()

        # WHEN
        result_filename, now = datasets.transform_and_write_to_file(test_dict)

        # THEN
        self.assertTrue(os.path.exists(result_filename))
        result_dict = petl.fromcsv(result_filename).dicts().list()
        self.assertEqual(len(test_dict), len(result_dict))
        self.assertTrue("films" not in result_dict[0].keys())
        self.assertTrue("http" not in result_dict[0]["homeworld"])

    def test_aggregate_negative(self):
        self.assertRaises(ValueError, datasets.aggregate, None, [])
        self.assertRaises(ValueError, datasets.aggregate, "", [])
        self.assertRaises(ValueError, datasets.aggregate, TRANSFORMED_CSV_FILENAME, [])
        self.assertRaises(ValueError, datasets.aggregate, TRANSFORMED_CSV_FILENAME, ["unexpected_column_name"])

    def test_aggregate_single_column(self):
        result = datasets.aggregate(TRANSFORMED_CSV_FILENAME, "homeworld")
        self.assertEqual(5, len(result))

        top_result = result[0]
        self.assertEqual("Tatooine", top_result["homeworld"])
        self.assertEqual(8, top_result["count"])

    def test_aggregate_multiple_columns(self):
        result = datasets.aggregate(TRANSFORMED_CSV_FILENAME, "homeworld", "skin_color")
        self.assertEqual(9, len(result))

        top_result = result[0]
        self.assertEqual("Tatooine", top_result["homeworld"])
        self.assertEqual("light", top_result["skin_color"])
        self.assertEqual(3, top_result["count"])


if __name__ == "__main__":
    unittest.main()
