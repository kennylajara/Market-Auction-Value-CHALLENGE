from typing import Type

from dto import EquipmentBaseDTO, EquipmentYearValueDTO
from entity import Equipment


class EquipmentMapper:
    """
    Class for mapping between Equipment and Equipment DTOs.
    """

    @staticmethod
    def map(
        equipment: Equipment, to: Type[EquipmentBaseDTO], **kwargs
    ) -> EquipmentBaseDTO:
        """
        Function for mapping an equipment to the received DTO.
        """
        if to == EquipmentYearValueDTO:
            try:
                return EquipmentMapper._to_equipment_year_value_dto(
                    equipment, year=kwargs["year"]
                )
            except KeyError:
                raise ValueError("Missing required argument: year")
        else:
            raise ValueError("Invalid DTO type.")

    @staticmethod
    def _to_equipment_year_value_dto(
        equipment: Equipment, year: int
    ) -> EquipmentYearValueDTO:
        """
        Function that takes an Equipment object and returns an EquipmentYearDTO object.
        """
        try:
            market_value = (
                equipment.sale_details.cost * equipment.schedule[year].market_ratio
            )
            auction_value = (
                equipment.sale_details.cost * equipment.schedule[year].auction_ratio
            )
        except KeyError:
            market_value = (
                equipment.sale_details.cost * equipment.schedule.default_market_ratio
            )
            auction_value = (
                equipment.sale_details.cost * equipment.schedule.default_auction_ratio
            )

        return EquipmentYearValueDTO(
            equipment_id=equipment.id,
            year=year,
            market_value=market_value,
            auction_value=auction_value,
        )
