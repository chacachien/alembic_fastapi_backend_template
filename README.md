# Backend Template with FastAPI and Alembic

This repository provides a basic template for building a REST API using FastAPI with database management through SQLAlchemy and migrations handled by Alembic.

## Features

- **FastAPI:** A modern, fast (high-performance), and easy-to-use web framework for building APIs.
- **SQLAlchemy:** A powerful and flexible ORM (Object Relational Mapper) for interacting with databases.
- **Alembic:** A database migration tool that allows you to safely and easily manage changes to your database schema.
- **Poetry:** A dependency management and packaging tool for Python projects.
- **Docker:** Included for easy setup and development in a containerized environment.

## Project Structure

```
├── src
│   ├── main.py # Main application entry point
│   └── db
│       ├── base.py  # Base SQLAlchemy model definition
│       └── models.py # Database models
└──
└──

```

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/backend-template.git
   ```

2. **Install Dependencies:**

   ```bash
   cd backend-template
   poetry install
   ```

3. **Configure Database:**

   - Create a `.env` file in the root directory.
   - Set the following environment variables:
     ```
     DATABASE_URL=postgresql://user:password@host:port/database
     ```
   - Replace the values with your actual database credentials.

4. **Create Database Migrations:**

   - Run the following command to create the initial migration:
     ```bash
     alembic init migrations
     ```
   - Modify the `alembic.ini` file to set the correct database URL.

5. **Run the Application:**

   - Start the development server:
     ```bash
     poetry run uvicorn main:app --reload
     ```

6. **Access the API:**

   - The API will be available at `http://127.0.0.1:8000/docs` for interactive documentation.

## Database Migrations

- To create a new migration, use the following command:
   ```bash
   alembic revision --autogenerate -m "Add new table"
   ```
- To upgrade the database to the latest version:
   ```bash
   alembic upgrade head
   ```
- To downgrade the database to a previous version:
   ```bash
   alembic downgrade <revision_id>
   ```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Additional Notes

- This template is a basic starting point and can be further customized to meet your specific project requirements.
- Consider using a logging library (e.g., `uvicorn.logging`) for more comprehensive logging.
- Implement security measures (e.g., authentication, authorization) based on your application's needs.
