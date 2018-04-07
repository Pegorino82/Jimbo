from sqlalchemy import Column, Integer, ForeignKey

from sqlalchemy.orm import relationship

from server.db.clients.client import Client

from server.db.db_core import Base

print('contacts imported')


class Contact(Base):
    __tablename__ = 'Contacts'

    id = Column(Integer, autoincrement=True, primary_key=True)
    owner_id = Column(Integer, ForeignKey('Clients.client_id'))
    contact_id = Column(Integer, ForeignKey('Clients.client_id'))

    owner = relationship(Client, foreign_keys=[owner_id])
    contact = relationship(Client, foreign_keys=[contact_id])


if __name__ == '__main__':
    pass
