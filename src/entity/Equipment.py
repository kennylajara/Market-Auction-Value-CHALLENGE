from __future__ import annotations
from typing import Optional

from utils import Api


class Year:
    """
    Class for storing the year of a equipment's schedule.
    """

    def __init__(self, year: int, market_ratio: float, auction_ratio: float) -> None:
        self._year: int = year
        self._market_ratio: float = market_ratio
        self._auction_ratio: float = auction_ratio

    def __str__(self) -> str:
        return str(
            {
                "year": self._year,
                "market_ratio": self._market_ratio,
                "auction_ratio": self._auction_ratio,
            }
        )

    @property
    def auction_ratio(self) -> float:
        return self._auction_ratio

    @property
    def market_ratio(self) -> float:
        return self._market_ratio

    @property
    def year(self) -> int:
        return self._year


class Schedule:
    """
    Class for storing the schedule of a equipment.
    """

    def __init__(
        self,
        years: dict[int, Year] = {},
        default_market_ratio: float = 0.0,
        default_auction_ratio: float = 0.0,
    ):
        self._years: dict[int, Year] = years
        self._default_market_ratio: float = default_market_ratio
        self._default_auction_ratio: float = default_auction_ratio

    def __str__(self) -> str:
        return str({year: str(data) for year, data in self._years.items()})

    def __getitem__(self, year: int) -> Year:
        return self._years[year]

    def __setitem__(self, year: int, year_data: Year) -> None:
        self._years[year] = year_data

    @property
    def years(self) -> dict[int, Year]:
        return self._years

    @property
    def default_market_ratio(self) -> float:
        return self._default_market_ratio

    @property
    def default_auction_ratio(self) -> float:
        return self._default_auction_ratio


class SaleDetails:
    """
    Class for storing the sale details of a equipment.
    """

    def __init__(
        self, cost: float, retail_sale_count: int, auction_sale_count: int
    ) -> None:
        self._cost: float = cost
        self._retail_sale_count: int = retail_sale_count
        self._auction_sale_count: int = auction_sale_count

    def __str__(self) -> str:
        return str(
            {
                "cost": self._cost,
                "retail_sale_count": self._retail_sale_count,
                "retail_sale_value": self._auction_sale_count,
            }
        )

    @property
    def cost(self) -> float:
        return self._cost

    @property
    def retail_sale_count(self) -> int:
        return self._retail_sale_count

    @property
    def auction_sale_count(self) -> int:
        return self._auction_sale_count


class Classification:
    """
    Class for storing the classification of a equipment.
    """

    def __init__(self, category: str, subcategory: str, make: str, model: str) -> None:
        self._category: str = category
        self._subcategory: str = subcategory
        self._make: str = make
        self._model: str = model

    def __str__(self) -> str:
        return str(
            {
                "category": self._category,
                "subcategory": self._subcategory,
                "make": self._make,
                "model": self._model,
            }
        )

    @property
    def category(self) -> str:
        return self._category

    @property
    def subcategory(self) -> str:
        return self._subcategory

    @property
    def make(self) -> str:
        return self._make

    @property
    def model(self) -> str:
        return self._model


class Equipment:
    """
    Business model for a equipment.
    """

    def __init__(
        self,
        id: int,
        schedule: Schedule,
        sale_details: SaleDetails,
        classification: Classification,
    ) -> None:
        self._id: int = id
        self._schedule: Schedule = schedule
        self._sale_details: SaleDetails = sale_details
        self._classification: Classification = classification

    def __str__(self) -> str:
        return str(
            {
                "id": self._id,
                "schedule": str(self._schedule),
                "sale_details": str(self._sale_details),
                "classification": str(self._classification),
            }
        )

    @property
    def id(self) -> int:
        return self._id

    @property
    def schedule(self) -> Schedule:
        return self._schedule

    @property
    def sale_details(self) -> SaleDetails:
        return self._sale_details

    @property
    def classification(self) -> Classification:
        return self._classification

    @staticmethod
    def get_from_api(equipment_id: int) -> Equipment:
        """
        Get the data of the specified equipment from the API.
        """
        data = Api.call(equipment_id)

        if data is None:
            raise ValueError(f"Equipment with id {equipment_id} not found.")

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

        return Equipment(
            id=equipment_id,
            schedule=schedule,
            sale_details=sale_details,
            classification=classification,
        )
