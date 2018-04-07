from sqlalchemy import Column, Integer, String

from server.db.db_core import Base

print('client imported')


class Client(Base):
    __tablename__ = 'Clients'
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    account_name = Column(String(25), unique=True)
    password = Column(String(25))
    user_info = Column(String(100))

    def __repr__(self):
        password = ''.join(['*' for i in self.password])
        return '<client_id: {}\naccount_name: {}\npassword: {}\nuser_info: {}>'.format(self.client_id,
                                                                                       self.account_name, password,
                                                                                       self.user_info)


if __name__ == '__main__':

    s_password = 'password'
    password = ''.join(['*' for i in s_password])

    print(password)