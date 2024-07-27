from typing import List
from qdrant_client import models, QdrandClient

from ..vector_db_interface import VectorDBInterface
from ..vector_db_enums import DistanceMethodEnums

import logging

class QdrantDBProvider(VectorDBInterface):
    def __init__(self, db_path: str, distance_method: str):

        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT
        
        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrandClient(path = self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)


    def list_all_collection(self, collection_name: str) -> List:
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name = collection_name)

    def remove_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name=collection_name): 
            return self.client.delete_collection(collection_name=collection_name)



    def create_collection(
        self, collection_name: str, 
        embedding_size: int, 
        do_reset: bool=False
    ):
        if do_reset: 
           _ = self.delete_collection(collection_name=collection_name)
        if not self.is_collection_existed(collection_name=collection_name):
            _ = self.client.create_collection(
            collection_name = collection_name,
            vector_config = models.VectorParams(
                size = embedding_size, 
                distance  = self.distance_method
                )
            )
            return True
        return False
    def insert_one(
        self, collection_name: str, 
        text: str, vector: list, 
        metadata:dict = None, 
        record_id: str=None
    ):
        if not self.is_collection_existed(collection_name):
            self.logger.error(f"Can not insert new record to non-existed collection: {collection_name}")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=[record_id],
                        vector=vector,
                        payload={
                            "text": text, "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting batch: {e}")
            return False

        return True

    def insert_many(
        self, collection_name: str, 
        texts: list, vector: list, 
        metadata:list = None, 
        record_id: list=None, 
        batch_size: int=50
    ):
        if metadata == None: metadata = [None]* len(texts)
        if record_id == None: record_id = [None]* len(texts)

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vector[i:batch_end]
            batch_metadata = metadata[i:batch_end]

            batch_records = [
                models.Record(
                    vector=batch_vectors[x], 
                    payload = {
                        "text": batch_texts[x], 
                        "metadata": batch_metadata[x]
                    }
                )

                for x in range(len(batch_texts))
            ]
            try: 
                _ = self.client.upload_records( 
                    collection_name=collection_name,
                    records=batch_records
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False

        return True


    def search_by_vector(
        self, collection_name: str, 
        vector: list, limit: int=5
    ):
        return self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
        )