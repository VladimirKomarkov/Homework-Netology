import sqlalchemy as sq
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    book = relationship("Book", back_populates='publisher')

    def __str__(self):
        return f"{self.id}: {self.name}"


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=255), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, ForeignKey('publisher.id'))

    publisher = relationship("Publisher", back_populates='book')

    def __str__(self):
        return f"{self.id}: ({self.title}, {self.id_publisher})"


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, ForeignKey('book.id'))
    id_shop = sq.Column(sq.Integer, ForeignKey('shop.id'))
    count = sq.Column(sq.Integer, nullable=False)

    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f"{self.id}: ({self.id_book}, {self.id_shop}, {self.count})"


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, ForeignKey('stock.id'))
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sale")

    def __str__(self):
        return f"{self.id}: ({self.price}, {self.date_sale}, {self.id_stock}, {self.count})"


def create_tables(engine):
    Base.metadata.create_all(engine)