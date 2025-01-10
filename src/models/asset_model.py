from sqlalchemy import select
from .base_data_model import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
class AssetModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client 
    @classmethod
    async def create_instance(cls, db_client): 
        instance = cls(db_client)
        return instance

    async def create_asset(self, asset: Asset):
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            session.commit()
            session.refresh(asset)
        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str): 
        async with self.db_client() as session: 
            statment = select(Asset).where(
                Asset.asset_project_id==asset_project_id,
                Asset.asset_type==asset_type
            )
            resutls = await session.execute(statment)
            if resutls is None: return None 
            # try: 
            records = resutls.scalars().all()
            # except Exception as e:
                # print(e)
                # return None
        return records

    async def get_asset_record(self, asset_project_id: str, asset_name: str):

        async with self.db_client() as session:
            stmt = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_name == asset_name
            )
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
        return record

