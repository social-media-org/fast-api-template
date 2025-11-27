"""Example service containing business logic."""

from typing import List

from app.core.logging import get_logger
from app.models.example_model import (
    ExampleCreate,
    ExampleInDB,
    ExampleResponse,
    ExampleUpdate,
)
from app.repositories.example_repository import ExampleRepository

logger = get_logger(__name__)


class ExampleService:
    """Service for Example business logic.
    
    Implements business rules and orchestrates repository operations.
    Separates business logic from API layer.
    """

    def __init__(self, repository: ExampleRepository) -> None:
        """Initialize service with repository dependency.

        Args:
            repository: Example repository instance
        """
        self.repository = repository

    async def create_example(self, example: ExampleCreate) -> ExampleResponse:
        """Create a new example.

        Args:
            example: Example data to create

        Returns:
            ExampleResponse: Created example
        """
        logger.info(f"Creating new example: {example.name}")
        created = await self.repository.create(example)
        logger.info(f"Example created with id: {created.id}")
        return ExampleResponse(**created.model_dump())

    async def get_example_by_id(self, example_id: str) -> ExampleResponse:
        """Get example by ID.

        Args:
            example_id: Example UUID

        Returns:
            ExampleResponse: Example data
        """
        logger.info(f"Fetching example with id: {example_id}")
        example = await self.repository.get_by_id(example_id)
        return ExampleResponse(**example.model_dump())

    async def list_examples(self, skip: int = 0, limit: int = 100) -> List[ExampleResponse]:
        """List all examples with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[ExampleResponse]: List of examples
        """
        logger.info(f"Listing examples (skip={skip}, limit={limit})")
        examples = await self.repository.get_all(skip=skip, limit=limit)
        return [ExampleResponse(**ex.model_dump()) for ex in examples]

    async def update_example(self, example_id: str, example: ExampleUpdate) -> ExampleResponse:
        """Update an existing example.

        Args:
            example_id: Example UUID
            example: Updated example data

        Returns:
            ExampleResponse: Updated example
        """
        logger.info(f"Updating example with id: {example_id}")
        updated = await self.repository.update(example_id, example)
        logger.info(f"Example updated: {example_id}")
        return ExampleResponse(**updated.model_dump())

    async def delete_example(self, example_id: str) -> bool:
        """Delete an example.

        Args:
            example_id: Example UUID

        Returns:
            bool: True if deleted successfully
        """
        logger.info(f"Deleting example with id: {example_id}")
        result = await self.repository.delete(example_id)
        logger.info(f"Example deleted: {example_id}")
        return result
