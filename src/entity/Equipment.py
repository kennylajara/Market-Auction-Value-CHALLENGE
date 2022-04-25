from __future__ import annotations
from dataclasses import dataclass, field

from utils import Api


@dataclass
class Year:
    """
    Class for storing the year of a equipment's schedule.
    """

    year: int
    market_ratio: float
    auction_ratio: float

    def __str__(self) -> str:
        return str(
            {
                "year": self.year,
                "market_ratio": self.market_ratio,
                "auction_ratio": self.auction_ratio,
            }
        )


@dataclass
class Schedule:
    """
    Class for storing the schedule of a equipment.
    """

    years: dict[int, Year] = field(default_factory=dict)
    default_market_ratio: float = 0.0
    default_auction_ratio: float = 0.0

    def __str__(self) -> str:
        return str({year: str(data) for year, data in self.years.items()})

    def __getitem__(self, year: int) -> Year:
        return self.years[year]

    def __setitem__(self, year: int, year_data: Year) -> None:
        self.years[year] = year_data


@dataclass
class SaleDetails:
    """
    Class for storing the sale details of a equipment.
    """

    cost: float
    retail_sale_count: int
    auction_sale_count: int

    def __str__(self) -> str:
        return str(
            {
                "cost": self.cost,
                "retail_sale_count": self.retail_sale_count,
                "retail_sale_value": self.auction_sale_count,
            }
        )


@dataclass
class Classification:
    """
    Class for storing the classification of a equipment.
    """

    category: str
    subcategory: str
    make: str
    model: str

    def __str__(self) -> str:
        return str(
            {
                "category": self.category,
                "subcategory": self.subcategory,
                "make": self.make,
                "model": self.model,
            }
        )


@dataclass
class Equipment:
    """
    Business model for a equipment.
    """

    id: int
    schedule: Schedule
    sale_details: SaleDetails
    classification: Classification

    def __str__(self) -> str:
        return str(
            {
                "id": self.id,
                "schedule": str(self.schedule),
                "sale_details": str(self.sale_details),
                "classification": str(self.classification),
            }
        )

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
