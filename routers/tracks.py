import aiosqlite
from fastapi import APIRouter, Depends, Response, status
from database import get_db_conn
from pydantic import BaseModel

router = APIRouter()

class AlbumPostRequest(BaseModel):
    title: str
    artist_id: int


@router.get("/tracks")
async def get_tracks(page: int = 0, per_page: int = 10,
                     connection: aiosqlite.Connection = Depends(get_db_conn)):
    connection.row_factory = aiosqlite.Row
    cursor = await connection\
        .execute("SELECT * FROM tracks ORDER BY tracks.TrackId ASC LIMIT ? OFFSET ?", (per_page, page * per_page))
    return await cursor.fetchall()


@router.get("/tracks/composers")
async def get_composers(composer_name: str, response: Response, connection: aiosqlite.Connection = Depends(get_db_conn)):

    connection.row_factory = lambda cursor, x: x[0]
    cursor = await connection.execute("SELECT Name, Composer FROM tracks WHERE Composer = ? ORDER BY Name ASC",
                                      (composer_name, ))
    tracks = await cursor.fetchall()

    if len(tracks) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "No tracks of given composer"}}
    else:
        return tracks


