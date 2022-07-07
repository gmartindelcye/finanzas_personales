# coding: utf-8
from typing import Optional, List
from datetime import date

from sqlmodel import Field, SQLModel, ForeignKey, Relationship, Enum


class AccountType(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str


class Institution(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True)
    name: str = Field(max_length=30)
    notes: str


class TransferType(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=15)


class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(max_length=5, unique=True)
    name: str = Field(max_length=100)
    password: str = Field(max_length=100)
    email: str = Field(max_length=50)
    notes: Optional[str]


class Nature(str, Enum):
    INCOME = 'Income'
    EXPENSE = 'Expense'

class Concept(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(max_length=10, unique=True)
    description: str = Field(max_length=30)

    nature: Nature 
 
    id_user = Field(foreignKey='user.id')

    user: User = Relationship(back_populates='concept')


class Account(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(max_length=5,  unique=True)
    balance: float = Field(server_default=0)
    cutting_day: Optional[int]
    pay_day: Optional[int]
    credit_limit: Optional[float]

    id_institution = Field(foreignKey='institution.id')
    id_accounttype = Field(foreignKey='accounttype.id')
    id_user = Field(foreignKey='user.id')

    accounttype: AccountType = Relationship(back_populates='account')
    institution: Institution = Relationship(back_populates='account')
    user: User = Relationship(back_populates='account')

    movements: Optional[List['Movement']] = Relationship(back_populates='account')
    origin_tfrs: Optional[List['Transfer']] = Relationship(back_populates='account')
    destin_tfrs: Optional[List['Transfer']] = Relationship(back_populates='account')


class Movement(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    datemov: date
    amount: float
    notes: Optional[str]
    documents: Optional[str]
    processed: bool = Field(server_default=False)

    id_user = Field(foreignKey='user.id')
    id_concept = Field(foreignKey='concept.id')
    id_account = Field(foreignKey='account.id')

    account: Account = Relationship(back_populates='movement')
    concept: Concept = Relationship(back_populates='movement')
    user: User = Relationship(back_populates='movement')


class Transfer(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    processed: bool = Field(server_default=False)

    id_user = Field(foreignKey='user.id')
    id_transfertype = Field(foreignKey='transfertype.id')
    id_origin_account = Field(fForeignKey='account.id')
    id_destination_account = Field(foreignKey='account.id')

    destination: Account = Relationship(back_populates='transfer')
    origin: Account = Relationship(back_populates='transfer')
    transfertype: TransferType = Relationship(back_populates='transfer')
    user: User = Relationship(back_populates='transfer')
