from sqlalchemy import delete, select
from .base_data_model import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance


    async def create_chunk(self, chunk: DataChunk):
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            session.commit()
            session.refresh()
        return chunk

    async def get_chunk(self, chunk_id: str):
        async with self.db_client() as session:
            results = session.execute(select(DataChunk).where(DataChunk.chunk_id==chunk_id))
            chunk = results.scalar_one_or_none()
        return chunk
        

    async def insert_many_chunks(self, chunks: list, batch_size: int=100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i+batch_size]
                    session.add_all(batch)
            session.commit()
        return len(chunks)


    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        async with self.db_client() as session:
            stetment = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
            resutls = await session.execute(stetment)
            await session.commit()
        return resutls.rowcount
    
    async def get_poject_chunks(self, project_id: ObjectId, page_no: int=1, page_size: int=50):
        async with self.db_client() as session:
            stetment = select(DataChunk).where(DataChunk.chunk_project_id==project_id).offset((page_no -1 )* page_size).limit(page_size)
            results = await session.execute(stetment)
            records = results.scalars().all()
        return records