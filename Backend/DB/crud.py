from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def create_data_entry(db: AsyncSession, data_entry: schemas.DataEntryCreate):
    queries = [item[0] for item in data_entry.data]
    img_links = [item[1] for item in data_entry.data]
    
    db_entry = models.DataEntry(
        description=data_entry.description,
        queries=",".join(queries),
        img_links=",".join(img_links)
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

async def get_data_entry(db: AsyncSession, entry_id: int):
    result = await db.execute(select(models.DataEntry).filter(models.DataEntry.id == entry_id))
    db_entry = result.scalars().first()
    if db_entry:
        db_entry.queries = db_entry.queries.split(",") if db_entry.queries else []
        db_entry.img_links = db_entry.img_links.split(",") if db_entry.img_links else []
    return db_entry

async def get_image_items(db: AsyncSession, id: int):
    result = await db.execute(select(models.DataEntry).filter(models.DataEntry.id == id))
    data_entry = result.scalars().first()
    if not data_entry:
        return []

    queries = data_entry.queries.split(',')
    img_links = data_entry.img_links.split(',')

    image_items = [
        models.ImageItem(name=query, url=img_link)
        for query, img_link in zip(queries, img_links)
    ]
    return image_items