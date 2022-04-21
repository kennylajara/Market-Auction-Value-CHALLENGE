from typing import Union, cast

from entity import Equipment
from dto import EquipmentYearValueDTO
from mapper import EquipmentMapper


def get_equiment_year_values(
    equipment_id: int, year: int
) -> Union[EquipmentYearValueDTO, ValueError]:
    """
    Function that takes the equipment id and year, and returns an object
    containing the calculated values (Market and Auction).
    """
    try:
        equipment = Equipment.get_from_api(equipment_id)
    except ValueError as e:
        return e

    equipment_year_value = cast(
        EquipmentYearValueDTO,
        EquipmentMapper.map(equipment, to=EquipmentYearValueDTO, year=year),
    )

    return equipment_year_value


if __name__ == "__main__":

    cases = [
        # Valid equipment id and year
        {
            "equipment_id": 67352,
            "year": 2007,
        },
        # Invalid equipment id
        {
            "equipment_id": 78964,
            "year": 2011,
        },
        # Invalid year (use the default market and auction ratio)
        {
            "equipment_id": 67352,
            "year": 2030,
        },
    ]

    for case in cases:
        result = get_equiment_year_values(case["equipment_id"], case["year"])
        print(repr(result))
        print("-" * 20)
