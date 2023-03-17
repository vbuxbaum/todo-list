<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-044a64?style=flat&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-00CCB8?style=flat&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/PyTest-6DB33F?style=flat&logo=pytest&logoColor=white">
</p>

# To-do List FastAPI

This API manages Users, Boards and to-do list Items. Every Item is associated to a Board, which is associated to an User. Only logged Users can edit their Boards and Items, and JWT is used for that.

The initial project architecture is based on a suggestion from ChatGPT

## Run the project

Install dependencies (you should do it in a [virtual environment](https://docs.python.org/3/library/venv.html)). It requires Python 3.10
```bash
pip install -r dev-requirements.txt
```

Run tests:
```bash
python -m pytest
```

Launch the server:
```bash
uvicorn app.main:app --reload
```

## Brief ChatGPT's Explanation of Each Component (with adjustments)

- `app/routes/` is where you define the FastAPI routes for your to-do list API.
- `app/core/` is where you define the business logic and entities of your to-do list application. This includes the `models.py` file where you define the data models for your to-do list items and the `services.py` file where you define the service functions that interact with the database.
- `app/infrastructure/` is where you define the low-level details for your to-do list application, such as the database connection. In this example, it contains a single `database.py` file, but you can add more files as needed.
- `app/main.py` is the entry point for your to-do list application.
- `tests/` is where you keep the test files for your to-do list application.

> This is just one possible structure for a clean architecture for a simple to-do list application with FastAPI. You can customize it to fit your specific requirements and add more components as needed.

