from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Checkpoint(Base):
    __tablename__ = 'checkpoints'
    id = Column(Integer, primary_key=True)
    label = Column(String(50))
    image = Column(LargeBinary, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)


class SessionHandler:
    __instance = None
    __initialized = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            self.engine = create_engine("sqlite:///checkpoints.db")
            self.Session = sessionmaker(bind=self.engine)
            SessionHandler.initialized = True

    def make_session(self):
        return self.Session()


engine = create_engine("sqlite:///checkpoints.db")
Base.metadata.create_all(engine)
