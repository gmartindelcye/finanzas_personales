from re import S
from sqlmodel import SQLModel, Session, create_engine, select

from models import Account, AccountType, Institution, Movement, User, Transfer, TransferType, Concept

# DB_URL = "sqlite:///finanzas_personales.db"
DB_URL = "sqlite:///test.db"
engine = create_engine(DB_URL)


def get_account_types():
    with Session(engine) as session:
        statement = select(AccountType)
        account_types = session.exec(statement).all()
        print(account_types)

def create_database():
    SQLModel.metadata.create_all(engine)

def main():
    create_database()

if __name__ == '__main__':
    main()