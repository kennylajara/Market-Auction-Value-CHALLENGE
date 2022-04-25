from dataclasses import dataclass


@dataclass(frozen=True)
class EquipmentBaseDTO:
    """
    Base class for Equipment DTOs.
    """

    equipment_id: int


@dataclass(frozen=True)
class EquipmentYearValueDTO(EquipmentBaseDTO):
    """
    Class for storing calculated values of a equipment.
    """

    year: int
    market_value: float
    auction_value: float

    def __str__(self):
        return str(
            {
                "equipment_id": self.equipment_id,
                "year": self.year,
                "market_value": self.market_value,
                "auction_value": self.auction_value,
            }
        )
