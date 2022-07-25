# Yandex Photos Parser

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Изменение конфига
```python
WORKER_NUMBER = 5  # Количество потоков для парсинга
FILENAME = "1.html"  # Имя файла на скачанный .html прогруженной страницы Яндекс.Картинки
```

## 3. Запуск приложения

```bash
python3 yandex_photos_parser.py
```