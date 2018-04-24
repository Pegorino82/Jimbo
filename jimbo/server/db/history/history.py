from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..clients.client import Client
from ..db_core import Base

print('history imported')


class History(Base):
    __tablename__ = 'History'

    id = Column(Integer, autoincrement=True, primary_key=True)
    time = Column(String)
    client_id = Column(Integer, ForeignKey('Clients.client_id'))
    action = Column(String)

    client = relationship(Client, foreign_keys=[client_id])


if __name__ == '__main__':
    pass
