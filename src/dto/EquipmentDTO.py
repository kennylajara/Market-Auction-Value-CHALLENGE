from typing import Union


class EquipmentBaseDTO:
    """
    Base class for Equipment DTOs.
    """

    def __init__(self, equipment_id: int) -> None:
        self._equipment_id: int = equipment_id

    @property
    def equipment_id(self) -> int:
        return self._equipment_id


class EquipmentYearValueDTO(EquipmentBaseDTO):
    """
    Class for storing calculated values of a equipment.
    """

    def __init__(
        self, equipment_id: int, year: int, market_value: float, auction_value: float
    ) -> None:
        super().__init__(equipment_id)
        self._year: int = year
        self._market_value: float = market_value
        self._auction_value: float = auction_value

    def __str__(self):
        return str(
            {
                "equipment_id": self._equipment_id,
                "year": self._year,
                "market_value": self._market_value,
                "auction_value": self._auction_value,
            }
        )

    def __repr__(self) -> str:
        attrs: dict[str, Union[int, float]] = {
            "equipment_id": self._equipment_id,
            "year": self._year,
            "market_value": self._market_value,
            "auction_value": self._auction_value,
        }
        attrs_str: str = ", ".join([f"{key}: {value}" for key, value in attrs.items()])
        return f"EquipmentYearValueDTO({attrs_str})"

    @property
    def year(self) -> int:
        return self._year

    @property
    def market_value(self) -> float:
        return self._market_value

    @property
    def auction_value(self) -> float:
        return self._auction_value
