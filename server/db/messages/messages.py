from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from server.db.clients.client import Client
from server.db.db_core import Base

print('messages imported')


class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, autoincrement=True, primary_key=True)
    message_time = Column(String)
    client_id = Column(Integer, ForeignKey('Clients.client_id'))
    target_id = Column(Integer, ForeignKey('Clients.client_id'))
    message = Column(String(500))

    client = relationship(Client, foreign_keys=[client_id])
    target = relationship(Client, foreign_keys=[client_id])


if __name__ == '__main__':
    pass
