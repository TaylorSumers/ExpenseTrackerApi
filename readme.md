# Expense Tracker API

Backend-сервис для учета личных доходов и расходов.

## Стек

- Python
- Flask
- SQLAlchemy
- Alembic
- SQLite (локально)

## Функциональность MVP

- регистрация пользователя
- аутентификация
- категории операций
- транзакции доходов и расходов
- бюджеты по категориям
- месячный отчет

## Требования

- Python 3.13+
- PowerShell (Windows) или совместимая оболочка

## Установка

1. Создать и активировать виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Установить зависимости:

```powershell
pip install -r requirements.txt
```

3. Создать локальный .env на основе шаблона:

```powershell
Copy-Item .env.example .env
```

4. При необходимости отредактировать .env.