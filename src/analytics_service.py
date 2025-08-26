from datetime import datetime, date, timedelta
from typing import Dict, Any
from src.repo.analytics_repo import AnalyticsRepository
from src.schemas import SalesTrendResponse, InventoryResponse, Dataset


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepository):
        self.repo = repo

    def sales_trend_chart(self, org_id: int, start: datetime, end: datetime) -> SalesTrendResponse:
        """Get sales trend data for chart visualization."""

        raw = self.repo.get_sales_trend(org_id, start, end)

        # Normalize data for charting
        start_date = start.date()
        end_date = end.date()
        days = (end_date - start_date).days + 1
        date_index = [start_date + timedelta(days=i) for i in range(days)]

        # create a dictionary with dates as keys and total_sales as values
        # this is done by looping through each tuple in raw and populate the sales_map dictionary
        sales_map = {}

        for entry in raw:
            date, total_sales = entry
            sales_map[date] = float(total_sales)

        # create a list of labels and data for the chart
        labels = [d.isoformat() for d in date_index]
        data = [sales_map.get(d, 0.0) for d in date_index]

        return SalesTrendResponse(
            labels=labels,
            datasets=[{"label": "sales", "data": data}]
        )
    
    def inventory_chart(self, org_id: int) -> InventoryResponse:
        """Get inventory levels for chart visualization."""
        raw = self.repo.get_inventory_levels(org_id) 
        if raw:
            name, _ = raw[0]            # Get the first product name to check if data exists
            labels = [name]
        else:
            labels = []

        data = [quantity for _, quantity in raw]

        return InventoryResponse(
            labels=labels,
            datasets=[{"label": "inventory", "data": data}]
        )

    def sales_avg(self, org_id: int, start: datetime, end: datetime) -> Dataset:
        """Get summary of sales data."""
        avg_sales = self.repo.get_sales_avg(org_id, start, end)
        
        return Dataset(label="avg_sales", data=[avg_sales])