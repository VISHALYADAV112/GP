# Database Migrations

This directory contains Alembic migrations for database schema versioning.

## Setup Alembic

```bash
cd db-schemas
pip install alembic
alembic init migrations
```

## Create Migration

```bash
alembic revision --autogenerate -m "description"
```

## Apply Migration

```bash
alembic upgrade head
```

## Rollback Migration

```bash
alembic downgrade -1
```
