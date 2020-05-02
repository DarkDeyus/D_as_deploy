import aiosqlite
from fastapi import APIRouter, Depends, Response, status
from database import get_db_conn
from pydantic import BaseModel

router = APIRouter()


@router.get("/sales")
async def create_album(category: str, response: Response,
                       connection: aiosqlite.Connection = Depends(get_db_conn)):

    if category == "customers":
        connection.row_factory = aiosqlite.Row
        cursor = await connection.execute("SELECT invoices.CustomerId, customers.Email, customers.Phone,"
                                          " ROUND(SUM(invoices.Total), 2) as Sum FROM invoices"
                                          " JOIN customers ON invoices.CustomerId = customers.CustomerId"
                                          " GROUP BY invoices.CustomerId"
                                          " ORDER BY Sum DESC, invoices.CustomerId")
        stats = await cursor.fetchall()
        return stats

    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "Given category does not exist"}}


