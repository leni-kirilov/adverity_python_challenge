import unittest
import os

from core.models import Dataset
from core.services import datasets, swapi


class End2EndTestCase(unittest.TestCase):
    """
    This integration test makes actual API calls, OS file writes and DB writes/reads
    """
    db_dataset = None

    def tearDown(self):
        if self.db_dataset:
            os.remove(self.db_dataset.filename)
            self.db_dataset.delete()

    def test_e2e_pull_transform_persist(self):
        # given some preexisting records in db
        db_records_before_test = len(Dataset.objects.all())

        self.db_dataset = datasets.fetch_transform_persist()

        self.assertTrue(self.db_dataset.id != 0)

        self.assertTrue(self.db_dataset.filename is not None)
        self.assertTrue(os.path.exists(self.db_dataset.filename))

        self.assertTrue(self.db_dataset.date_created is not None)
        self.assertEqual(db_records_before_test + 1, len(Dataset.objects.all()))


if __name__ == "__main__":
    unittest.main()
