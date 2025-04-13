import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Publisher, Book, Shop, Stock, Sale
from datetime import datetime

# Настройка подключения к базе данных
DATABASE_URL = 'postgresql://postgres:skazka@localhost/library_db'
engine = create_engine(DATABASE_URL, echo=True)

# Создаем таблицы (если их нет)
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()


# Функция для загрузки данных из JSON-файла
def load_data_from_json(file_path, model_class):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Создаем экземпляры модели и добавляем их в сессию
        for item in data:
            if "date_sale" in item:
                item["date_sale"] = datetime.fromisoformat(item["date_sale"])
            instance = model_class(**item)
            session.add(instance)

        print(f"Данные из {file_path} успешно загружены.")
    except Exception as e:
        print(f"Ошибка при загрузке данных из {file_path}: {e}")


# Загрузка данных для каждой таблицы
if __name__ == "__main__":
    # Очистка таблиц перед загрузкой новых данных (опционально)
    session.query(Sale).delete()
    session.query(Stock).delete()
    session.query(Book).delete()
    session.query(Shop).delete()
    session.query(Publisher).delete()
    session.commit()

    # Путь к папке fixtures
    fixtures_dir = "fixtures"

    # Загружаем данные для каждой таблицы
    load_data_from_json(f"{fixtures_dir}/publisher.json", Publisher)
    load_data_from_json(f"{fixtures_dir}/book.json", Book)
    load_data_from_json(f"{fixtures_dir}/shop.json", Shop)
    load_data_from_json(f"{fixtures_dir}/stock.json", Stock)
    load_data_from_json(f"{fixtures_dir}/sale.json", Sale)

    # Сохраняем изменения в базе данных
    session.commit()

    # Закрываем сессию
    session.close()


