"""Dependency injection for API layer."""

from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.main import get_database
from app.repositories.example_repository import ExampleRepository
from app.services.example_service import ExampleService


def get_example_repository(
    database: Annotated[AsyncIOMotorDatabase, Depends(get_database)]
) -> ExampleRepository:
    """Get Example repository instance with database dependency.

    Args:
        database: MongoDB database instance

    Returns:
        ExampleRepository: Repository instance
    """
    return ExampleRepository(database)


def get_example_service(
    repository: Annotated[ExampleRepository, Depends(get_example_repository)]
) -> ExampleService:
    """Get Example service instance with repository dependency.

    Args:
        repository: Example repository instance

    Returns:
        ExampleService: Service instance
    """
    return ExampleService(repository)
