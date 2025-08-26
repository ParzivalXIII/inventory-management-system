from datetime import datetime, date
from typing import List, Tuple, Sequence
from sqlmodel import  Session, select, func, text
from src.models import Order, Product


class AnalyticsRepository:
    """DB-only accessors for analytics. Keep logic here so services stay testable.

    Assumes Order has: id, created_at (datetime), quantity (int), price (float), organization_id (int)
    Assumes Product has: id, name, stock_quantity (int), organization_id (int)
    """

    def __init__(self, session: Session):
        self.session = session

    def get_sales_trend(self, org_id: int, start: date, end: date) -> List[Tuple[date, float]]:
        """Get daily sales totals for a date range."""
        query = (
            select(
                func.date(Order.order_date).label("date"),
                func.sum(Order.total_price).label("total_sales")
            )
            .where(Order.organization_id==org_id)
            .where(Order.order_date >= start)
            .where(Order.order_date <= end)
            .group_by(func.date(Order.order_date))
            .group_by(func.date(Order.order_date))
        )
        rows = self.session.exec(query).all()
        # rows are Row(date=<date>, total_sales=<Decimal|float>)

        result = [
            (row[0], float(row[1]))
            for row in rows
        ]
        return result
    
    def get_inventory_levels(self, org_id: int) -> List[Tuple[str, int]]:
        """Get current inventory levels for all products."""
        query = (
            select(
                Product.name,
                Product.quantity
            )
            .where(Product.organization_id==org_id)
            .order_by(Product.name)
        )

        # Execute the query and fetch all results
        rows = self.session.exec(query).all()
        result = [(str(row[0]), row[1]) for row in rows if row[1] is not None]
        return result
    
    def get_sales_avg(self, org_id: int, start: date, end: date) -> float:
        query = (
            select(func.coalesce(Order.total_price, 0).label("total_sales"))
            .where(Order.organization_id == org_id)
            .where(Order.order_date >= start)
            .where(Order.order_date <= end)
        )
        row = self.session.exec(query).one()
        return row