import aiosqlite
from fastapi import APIRouter, Depends, Response, status
from database import get_db_conn
from pydantic import BaseModel

router = APIRouter()

class AlbumPostRequest(BaseModel):
    title: str
    artist_id: int


@router.post("/albums")
async def create_album(request: AlbumPostRequest, response: Response, connection: aiosqlite.Connection = Depends(get_db_conn)):
    connection.row_factory = aiosqlite.Row

    cursor = await connection.execute("SELECT * FROM artists WHERE ArtistId IS ? ",
                                      (request.artist_id,))
    artist = await cursor.fetchall()

    if len(artist) != 1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "Artist of given id does not exist"}}

    await connection.execute("INSERT INTO albums VALUES (?, ?)", (request.title, request.artist_id))
    connection.commit()

    cursor = await connection.execute(
        "SELECT * FROM albums WHERE Title = ? AND ArtistId = ?", (request.title, request.artist_id))
    artist = await cursor.fetchone()
    response.status_code = status.HTTP_201_CREATED
    return artist

@router.get("/albums/{album_id}")
async def get_album(album_id: int, connection: aiosqlite.Connection = Depends(get_db_conn)):
    connection.row_factory = aiosqlite.Row

    cursor = await connection.execute("SELECT * FROM albums WHERE AlbumId = ?", (album_id, ))
    artist = await cursor.fetchone()
    return artist

