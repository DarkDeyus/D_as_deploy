import aiosqlite
from fastapi import APIRouter, Depends, Response, status
from database import get_db_conn
from pydantic import BaseModel

router = APIRouter()


class CustomerPutRequest(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None


@router.put("/customers/{customer_id}")
async def create_album(customer_id: int, request: CustomerPutRequest, response: Response,
                       connection: aiosqlite.Connection = Depends(get_db_conn)):

    connection.row_factory = aiosqlite.Row
    cursor = await connection.execute("SELECT Company AS company, Address as address, City as city, State as state,"
                                      " Country as country, PostalCode as postalcode, Fax as fax FROM customers"
                                      " WHERE CustomerId IS ? ", (customer_id,))
    customer = await cursor.fetchall()

    if len(customer) != 1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "Customer of given id does not exist"}}

    request_customer = CustomerPutRequest(**customer)
    update_data = request.dict(exclude_unset=True)
    updated = request_customer.copy(update=update_data)

    cursor = await connection.execute("UPDATE customers SET Company = ?, Address = ?, City = ?, State = ?, Country = ?,"
                                      " PostalCode = ?, Fax = ? WHERE CustomerId = ?", (updated.company,
                                                                                        updated.address,
                                                                                        updated.city,
                                                                                        updated.state,
                                                                                        updated.country,
                                                                                        updated.postalcode,
                                                                                        updated.fax,
                                                                                        customer_id))
    connection.commit()

    cursor = await connection.execute("SELECT * FROM customers WHERE CustomerId = ?", (customer_id, ))
    return await cursor.fetchone()





