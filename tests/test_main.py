from unittest import TestCase

from main import get_equiment_year_values
from dto import EquipmentYearValueDTO


# NOTE: Normally, we would mock the API call but, as we are already
#       using a mocked JSON file, we are not mocking it in any part
#       of this file.


class TestMainFunctions(TestCase):
    def test_get_equiment_year_values_with_data_contained_in_the_api_response(self):
        tests = [
            (
                {
                    "equipment_id": 67352,
                    "year": 2007,
                },
                {
                    "market_value": 216384.71025600002,
                    "auction_value": 126089.52642,
                },
            ),
            (
                {
                    "equipment_id": 67352,
                    "year": 2008,
                },
                {
                    "market_value": 220801.26697199998,
                    "auction_value": 128662.61522400001,
                },
            ),
            (
                {
                    "equipment_id": 87390,
                    "year": 2017,
                },
                {
                    "market_value": 33906.084485,
                    "auction_value": 23153.447444999998,
                },
            ),
        ]

        for test in tests:
            data, expected_value = test
            with self.subTest(data=data):
                equipment_details = get_equiment_year_values(
                    data["equipment_id"], data["year"]
                )
                self.assertIsInstance(
                    equipment_details,
                    EquipmentYearValueDTO,
                )
                self.assertEqual(
                    expected_value["market_value"],
                    equipment_details.market_value,
                )
                self.assertEqual(
                    expected_value["auction_value"],
                    equipment_details.auction_value,
                )

    def test_get_equiment_year_values_with_equipment_id_not_contained_in_the_api_response(
        self,
    ):
        tests = [
            {
                "equipment_id": 777,
                "year": 2010,
            },
            {
                "equipment_id": 123,
                "year": 2019,
            },
        ]

        for test in tests:
            with self.subTest(data=tests):
                equipment_details = get_equiment_year_values(
                    test["equipment_id"], test["year"]
                )
                self.assertIsInstance(
                    equipment_details,
                    ValueError,
                )
                self.assertEqual(
                    str(equipment_details),
                    f"Equipment with id {test['equipment_id']} not found.",
                )

    def test_get_equiment_year_values_with_year_not_contained_in_the_api_response(self):
        # NOTE: It is expected to return some data because it uses
        #       the default market ratio and auction ratio for the
        #       missing years.
        tests = [
            (
                {
                    "equipment_id": 67352,
                    "year": 1900,
                },
                {
                    "market_value": 13625.04,
                    "auction_value": 13625.04,
                },
            ),
            (
                {
                    "equipment_id": 67352,
                    "year": 2100,
                },
                {
                    "market_value": 13625.04,
                    "auction_value": 13625.04,
                },
            ),
            (
                {
                    "equipment_id": 87390,
                    "year": 3000,
                },
                {
                    "market_value": 2935.74,
                    "auction_value": 2935.74,
                },
            ),
        ]

        for test in tests:
            data, expected_value = test
            with self.subTest(data=data):
                equipment_details = get_equiment_year_values(
                    data["equipment_id"], data["year"]
                )
                self.assertIsInstance(
                    equipment_details,
                    EquipmentYearValueDTO,
                )
                self.assertEqual(
                    expected_value["market_value"],
                    equipment_details.market_value,
                )
                self.assertEqual(
                    expected_value["auction_value"],
                    equipment_details.auction_value,
                )
