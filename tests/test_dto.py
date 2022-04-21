from unittest import TestCase

from dto import EquipmentYearValueDTO


class TestEquipmentYearValueDTO(TestCase):
    def test_equipment_year_value_dto_has_correct_attributes(self):
        tests = [
            (67352, 2007, 216384.71025600002, 126089.52642),
            (67352, 2008, 220801.26697199998, 128662.61522400001),
            (87390, 2017, 33906.084485, 23153.447444999998),
        ]

        for test in tests:
            equipment_id, year, market_value, auction_value = test

            equipment_year_value_dto = EquipmentYearValueDTO(
                equipment_id=equipment_id,
                year=year,
                market_value=market_value,
                auction_value=auction_value,
            )

            self.assertIsInstance(equipment_year_value_dto, EquipmentYearValueDTO)
            self.assertEqual(equipment_year_value_dto.equipment_id, equipment_id)
            self.assertEqual(equipment_year_value_dto.year, year)
            self.assertEqual(equipment_year_value_dto.market_value, market_value)
            self.assertEqual(equipment_year_value_dto.auction_value, auction_value)
