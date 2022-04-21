import json, os
from unittest import TestCase

from entity import Classification, Equipment, SaleDetails, Schedule, Year


# NOTE: Normally, we would mock the API call but, as we are already
#       using a mocked JSON file, we are not mocking it here.


class TestEquipment(TestCase):
    def test_equipment_is_properly_initialized_from_api(self):

        # load tests from json file
        with open(os.path.join(os.getcwd(), "data", "api-response.json"), "r") as f:
            test_data = json.load(f)

        for equipment_id, data in test_data.items():

            equipment = Equipment.get_from_api(equipment_id=equipment_id)

            # Equipment
            self.assertIsInstance(equipment, Equipment)
            self.assertEqual(equipment.id, equipment_id)

            # Classification
            self.assertIsInstance(equipment.classification, Classification)
            self.assertEqual(
                equipment.classification.category, data["classification"]["category"]
            )
            self.assertEqual(
                equipment.classification.subcategory,
                data["classification"]["subcategory"],
            )
            self.assertEqual(
                equipment.classification.make, data["classification"]["make"]
            )
            self.assertEqual(
                equipment.classification.model, data["classification"]["model"]
            )

            # SaleDetails
            self.assertIsInstance(equipment.sale_details, SaleDetails)
            self.assertEqual(equipment.sale_details.cost, data["saleDetails"]["cost"])
            self.assertEqual(
                equipment.sale_details.retail_sale_count,
                data["saleDetails"]["retailSaleCount"],
            )
            self.assertEqual(
                equipment.sale_details.auction_sale_count,
                data["saleDetails"]["auctionSaleCount"],
            )

            # Schedule
            self.assertIsInstance(equipment.schedule, Schedule)
            self.assertIsInstance(equipment.schedule.years, dict)
            self.assertEqual(
                len(equipment.schedule.years), len(data["schedule"]["years"])
            )
            self.assertEqual(
                equipment.schedule.default_market_ratio,
                data["schedule"]["defaultMarketRatio"],
            )
            self.assertEqual(
                equipment.schedule.default_auction_ratio,
                data["schedule"]["defaultAuctionRatio"],
            )

            # Year
            for key, year in equipment.schedule.years.items():
                self.assertIsInstance(key, int)
                self.assertIsInstance(year, Year)
                self.assertEqual(year.year, key)
                self.assertEqual(
                    year.market_ratio,
                    data["schedule"]["years"][str(key)]["marketRatio"],
                )
                self.assertEqual(
                    year.auction_ratio,
                    data["schedule"]["years"][str(key)]["auctionRatio"],
                )

    def test_equipment_raise_value_error_if_not_found(self):
        with self.assertRaises(ValueError):
            Equipment.get_from_api(equipment_id=0)
