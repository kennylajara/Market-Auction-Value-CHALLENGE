import json, os
from unittest import TestCase

from dto import EquipmentYearValueDTO
from entity import Classification, Equipment, SaleDetails, Schedule, Year
from mapper import EquipmentMapper


class TestEquipmentMapper(TestCase):
    def test_equipment_mapper_maps_equipment_to_equipment_year_value_dto_when_the_id_and_year_are_valid(
        self,
    ):
        # load tests from json file
        with open(os.path.join(os.getcwd(), "data", "api-response.json"), "r") as f:
            test_data = json.load(f)

        for equipment_id, data in test_data.items():
            # Manually create an Equipment object (mapper input)
            schedule = Schedule(
                years={},
                default_market_ratio=data["schedule"]["defaultMarketRatio"],
                default_auction_ratio=data["schedule"]["defaultAuctionRatio"],
            )
            for year, year_details in data["schedule"]["years"].items():
                schedule[int(year)] = Year(
                    int(year), year_details["marketRatio"], year_details["auctionRatio"]
                )

            sale_details = SaleDetails(
                cost=data["saleDetails"]["cost"],
                retail_sale_count=data["saleDetails"]["retailSaleCount"],
                auction_sale_count=data["saleDetails"]["auctionSaleCount"],
            )

            classification = Classification(
                category=data["classification"]["category"],
                subcategory=data["classification"]["subcategory"],
                make=data["classification"]["make"],
                model=data["classification"]["model"],
            )

            equipment = Equipment(
                id=equipment_id,
                schedule=schedule,
                sale_details=sale_details,
                classification=classification,
            )

            # Manually create EquipmentYearValueDTO object (expected mapper output)
            test_year = list(schedule.years.keys())[0]
            expected_equipment_year_value_dto = EquipmentYearValueDTO(
                equipment_id=equipment_id,
                year=schedule.years[test_year].year,
                market_value=schedule.years[test_year].market_ratio * sale_details.cost,
                auction_value=schedule.years[test_year].auction_ratio
                * sale_details.cost,
            )

            # Map the Equipment object to a EquipmentYearValueDTO object
            actual_equipment_year_value_dto = EquipmentMapper.map(
                equipment=equipment,
                to=EquipmentYearValueDTO,
                year=test_year,
            )

            # Assert that the EquipmentYearValueDTO object is equal to the expected one
            self.assertEqual(
                expected_equipment_year_value_dto.equipment_id,
                actual_equipment_year_value_dto.equipment_id,
            )
            self.assertEqual(
                expected_equipment_year_value_dto.year,
                actual_equipment_year_value_dto.year,
            )
            self.assertEqual(
                expected_equipment_year_value_dto.market_value,
                actual_equipment_year_value_dto.market_value,
            )
            self.assertEqual(
                expected_equipment_year_value_dto.auction_value,
                actual_equipment_year_value_dto.auction_value,
            )

    def test_equipment_mapper_maps_equipment_to_equipment_year_value_dto_using_default_values_when_the_year_is_invalid(
        self,
    ):
        # load tests from json file
        with open(os.path.join(os.getcwd(), "data", "api-response.json"), "r") as f:
            test_data = json.load(f)

        for equipment_id, data in test_data.items():
            # Manually create an Equipment object (mapper input)
            schedule = Schedule(
                years={},
                default_market_ratio=data["schedule"]["defaultMarketRatio"],
                default_auction_ratio=data["schedule"]["defaultAuctionRatio"],
            )
            for year, year_details in data["schedule"]["years"].items():
                schedule[int(year)] = Year(
                    int(year), year_details["marketRatio"], year_details["auctionRatio"]
                )

            sale_details = SaleDetails(
                cost=data["saleDetails"]["cost"],
                retail_sale_count=data["saleDetails"]["retailSaleCount"],
                auction_sale_count=data["saleDetails"]["auctionSaleCount"],
            )

            classification = Classification(
                category=data["classification"]["category"],
                subcategory=data["classification"]["subcategory"],
                make=data["classification"]["make"],
                model=data["classification"]["model"],
            )

            equipment = Equipment(
                id=equipment_id,
                schedule=schedule,
                sale_details=sale_details,
                classification=classification,
            )

            # Manually create EquipmentYearValueDTO object (expected mapper output)
            test_year = 2030
            expected_equipment_year_value_dto = EquipmentYearValueDTO(
                equipment_id=equipment_id,
                year=test_year,
                market_value=schedule.default_market_ratio * sale_details.cost,
                auction_value=schedule.default_auction_ratio * sale_details.cost,
            )

            # Map the Equipment object to a EquipmentYearValueDTO object
            actual_equipment_year_value_dto = EquipmentMapper.map(
                equipment=equipment,
                to=EquipmentYearValueDTO,
                year=test_year,
            )

            # Assert that the EquipmentYearValueDTO object is equal to the expected one
            self.assertEqual(
                expected_equipment_year_value_dto.equipment_id,
                actual_equipment_year_value_dto.equipment_id,
            )
            self.assertEqual(
                expected_equipment_year_value_dto.year,
                actual_equipment_year_value_dto.year,
            )
            self.assertEqual(
                expected_equipment_year_value_dto.market_value,
                actual_equipment_year_value_dto.market_value,
            )
            self.assertEqual(
                expected_equipment_year_value_dto.auction_value,
                actual_equipment_year_value_dto.auction_value,
            )
