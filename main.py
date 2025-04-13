import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale
from datetime import datetime

# Загрузка параметров подключения из переменных окружения
DB_USER = os.getenv("DB_USER", "postgres")  # Логин для БД
DB_PASSWORD = os.getenv(
    "DB_PASSWORD", "db_password"
)  # Пароль для БД
DB_HOST = os.getenv("DB_HOST", "localhost")  # Хост БД
DB_NAME = os.getenv("DB_NAME", "library_db")  # Название БД

# Формирование строки подключения
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}/{DB_NAME}"
)

# Настройка подключения к базе данных
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()


def query_publisher_sales(publisher_name_or_id):
    # Определяем, является ли ввод именем или ID
    try:
        publisher_id = int(publisher_name_or_id)  # Если ввод — число, это ID
        publisher_filter = Publisher.id == publisher_id
    except ValueError:
        publisher_filter = Publisher.name.ilike(f"%{publisher_name_or_id}%")

    # Выполняем запрос
    results = (
        session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
        .join(Publisher, Book.id_publisher == Publisher.id)
        .join(Stock, Book.id == Stock.id_book)
        .join(Shop, Stock.id_shop == Shop.id)
        .join(Sale, Stock.id == Sale.id_stock)
        .filter(publisher_filter)
        .all()
    )

    # Выводим результаты
    if not results:
        print("Нет данных о покупках для этого издателя.")
    else:
        for book_title, shop_name, price, date_sale in results:
            # Проверяем, что дата существует и является объектом datetime
            if isinstance(date_sale, datetime):
                formatted_date = date_sale.strftime('%d-%m-%Y')
            else:
                formatted_date = "Дата не указана"

            # Выводим данные
            print(
                f"{book_title} | {shop_name} | {price} | "
                f"{formatted_date}"
            )


if __name__ == "__main__":
    # Запрашиваем у пользователя имя или ID издателя
    publisher_input = input("Введите имя или ID издателя: ")

    # Выполняем запрос и выводим результаты
    query_publisher_sales(publisher_input)

    # Закрываем сессию
    session.close()

