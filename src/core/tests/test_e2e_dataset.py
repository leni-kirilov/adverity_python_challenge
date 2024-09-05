import unittest
import os

from core.models import Dataset
from core.services import datasets, swapi


class End2EndTestCase(unittest.TestCase):
    """
    This integration test makes actual API calls, OS file writes and DB writes/reads
    """

    def test_e2e_pull_transform_persist(self):
        # given some preexisting records in db
        db_records_before_test = len(Dataset.objects.all())

        db_dataset = datasets.fetch_transform_persist()

        self.assertTrue(db_dataset.id != 0)

        self.assertTrue(db_dataset.filename is not None)
        self.assertTrue(os.path.exists(db_dataset.filename))

        self.assertTrue(db_dataset.date_created is not None)
        self.assertEqual(db_records_before_test + 1, len(Dataset.objects.all()))


if __name__ == "__main__":
    unittest.main()
