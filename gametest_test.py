import unittest
from building_manager import *


class TestBuildingManager(unittest.TestCase):
    def test_get_currently_building_name(self):
        self.assertEqual(BuildingManager.buildings_names_list[selection_id], "Air purifier")


if __name__ == '__main__':
    unittest.main()
