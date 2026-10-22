from abc import ABC, abstractmethod

from models.transport_collection_model import TransportCollection


class TransportCollectionRepositoryInterface(ABC):

    @abstractmethod
    def create(
        self, collection: TransportCollection
    ) -> TransportCollection:
        pass

    @abstractmethod
    def get_all(self) -> list[TransportCollection]:
        pass

    @abstractmethod
    def get_by_id(
        self, collection_id: int
    ) -> TransportCollection | None:
        pass

    @abstractmethod
    def update_collection(
        self,
        collection: TransportCollection,
        update_data: dict,
    ) -> TransportCollection:
        pass

    @abstractmethod
    def delete(self, collection: TransportCollection) -> None:
        pass