from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Создаем базовый класс для моделей
Base = declarative_base()


# Модель Publisher (Издатель)
class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Отношение один-ко-многим с Book
    books = relationship("Book", back_populates="publisher")

    def __repr__(self):
        return f"Publisher(id={self.id}, name='{self.name}')"


# Модель Book (Книга)
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    # Отношение многие-ко-многим с Shop через Stock
    stocks = relationship("Stock", back_populates="book")

    # Отношение один-ко-многим с Publisher
    publisher = relationship("Publisher", back_populates="books")

    def __repr__(self):
        return (
            f"Book(id={self.id}, title='{self.title}', "
            f"publisher_id={self.id_publisher})"
        )


# Модель Shop (Магазин)
class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Отношение многие-ко-многим с Book через Stock
    stocks = relationship("Stock", back_populates="shop")

    def __repr__(self):
        return f"Shop(id={self.id}, name='{self.name}')"


# Модель Stock (Наличие книги в магазине)
class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    # Отношение многие-ко-многим с Book и Shop
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")

    # Отношение один-ко-многим с Sale
    sales = relationship("Sale", back_populates="stock")

    def __repr__(self):
        return (
            f"Stock(id={self.id}, book_id={self.id_book}, "
            f"shop_id={self.id_shop}, count={self.count})"
        )


# Модель Sale (Факт продажи)
class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    date_sale = Column(DateTime, default=datetime.utcnow, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)

    # Отношение один-ко-многим с Stock
    stock = relationship("Stock", back_populates="sales")

    def __repr__(self):
        return (
            f"Sale(id={self.id}, price={self.price}, "
            f"date_sale='{self.date_sale}', "
            f"stock_id={self.id_stock}, count={self.count})"
        )

# <- Пустая строка в конце файла
