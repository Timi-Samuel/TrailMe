from src.models.model import Checkpoint, SessionHandler
from src.services.custom_exceptions import CheckpointNotFoundError, CheckPointAlreadyExistsError, NoTargetsFoundError


class CheckService:
    def __init__(self, id=None, label=None, image=None, latitude=None, longitude=None):
        self.__id = id
        self.__label = label
        self.__image = image
        self.__latitude = latitude
        self.__longitude = longitude

    @staticmethod
    def get_checkpoints():
        session = SessionHandler()
        session = session.make_session()
        targets = session.query(Checkpoint).all()
        if targets:
            if len(targets) > 0:
                return [[i.id, i.label, i.image, i.latitude, i.longitude] for i in targets]
        raise NoTargetsFoundError("No targets found")

    def add_checkpoint(self):
        checkpoint = Checkpoint(
            id=self.__id,
            label=self.__label,
            image=self.__image,
            latitude=self.__latitude,
            longitude=self.__longitude
        )

        session = SessionHandler()
        session = session.make_session()
        match = session.query(Checkpoint).filter_by(
            label=self.__label,
            latitude=self.__latitude,
            longitude=self.__longitude).first()

        if match:
            raise CheckPointAlreadyExistsError("Checkpoint Already Exists")
        session.add(checkpoint)
        session.commit()
        return

    def update_checkpoint(self):
        session = SessionHandler()
        session = session.make_session()
        target = session.query(Checkpoint).get(self.__id)
        if not target:
            raise CheckpointNotFoundError("Checkpoint Not Found")
        if self.__label is not None:
            target.label = self.__label
        if self.__image is not None:
            target.image = self.__image
        if self.__latitude is not None:
            target.latitude = self.__latitude
        if self.__longitude is not None:
            target.longitude = self.__longitude
        session.commit()
        return

    def delete_checkpoint(self):
        session = SessionHandler()
        session = session.make_session()
        target = session.query(Checkpoint).get(self.__id)
        if not target:
            raise CheckpointNotFoundError("Checkpoint Not Found")
        session.delete(target)
        session.commit()
        return

    def get_checkpoint(self):
        session = SessionHandler()
        session = session.make_session()
        target = session.query(Checkpoint).get(self.__id)

        if not target:
            raise CheckpointNotFoundError("Checkpoint Not Found")
        return {'lat': target.latitude, 'long': target.longitude}
