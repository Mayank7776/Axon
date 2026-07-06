# Skill: Create Migration

This skill outlines how to generate and execute Alembic database migrations after changes are made to database models.

## Guidelines

1. Make sure all models are imported inside `migrations/env.py`. Otherwise, Alembic's autogenerate command will not recognize your new tables or columns.
2. In the terminal, ensure you are in the `/Backend` directory and the virtual environment is activated.
3. Run the autogenerate revision command:
   ```bash
   alembic revision --autogenerate -m "Describe your database changes here"
   ```
4. Open the generated script located inside `Backend/migrations/versions/` to inspect and verify the `upgrade()` and `downgrade()` logic. Make sure standard PostgreSQL translations or defaults are correct.
5. Apply the migration to the PostgreSQL database:
   ```bash
   alembic upgrade head
   ```
6. If you need to roll back the migration, run:
   ```bash
   alembic downgrade -1
   ```
