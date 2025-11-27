"""Example repository for MongoDB operations."""

import uuid
from datetime import datetime
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import NotFoundException
from app.models.example_model import ExampleCreate, ExampleInDB, ExampleUpdate


class ExampleRepository:
    """Repository for Example entity operations.
    
    Implements data access layer with MongoDB using Repository pattern.
    """

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        """Initialize repository with database connection.

        Args:
            database: MongoDB database instance
        """
        self.collection = database["examples"]

    async def create(self, example: ExampleCreate) -> ExampleInDB:
        """Create a new example in database.

        Args:
            example: Example data to create

        Returns:
            ExampleInDB: Created example with database fields
        """
        now = datetime.utcnow()
        example_dict = example.model_dump()
        example_dict["id"] = str(uuid.uuid4())
        example_dict["created_at"] = now
        example_dict["updated_at"] = now

        await self.collection.insert_one(example_dict)
        return ExampleInDB(**example_dict)

    async def get_by_id(self, example_id: str) -> ExampleInDB:
        """Get example by ID.

        Args:
            example_id: Example UUID

        Returns:
            ExampleInDB: Example from database

        Raises:
            NotFoundException: If example not found
        """
        example_dict = await self.collection.find_one({"id": example_id})
        if not example_dict:
            raise NotFoundException(f"Example with id {example_id} not found")

        # Remove MongoDB _id field
        example_dict.pop("_id", None)
        return ExampleInDB(**example_dict)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ExampleInDB]:
        """Get all examples with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[ExampleInDB]: List of examples
        """
        cursor = self.collection.find().skip(skip).limit(limit)
        examples = []
        async for example_dict in cursor:
            example_dict.pop("_id", None)
            examples.append(ExampleInDB(**example_dict))
        return examples

    async def update(self, example_id: str, example: ExampleUpdate) -> ExampleInDB:
        """Update an existing example.

        Args:
            example_id: Example UUID
            example: Updated example data

        Returns:
            ExampleInDB: Updated example

        Raises:
            NotFoundException: If example not found
        """
        # Check if example exists
        await self.get_by_id(example_id)

        # Update only provided fields
        update_data = example.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await self.collection.update_one({"id": example_id}, {"$set": update_data})

        return await self.get_by_id(example_id)

    async def delete(self, example_id: str) -> bool:
        """Delete an example.

        Args:
            example_id: Example UUID

        Returns:
            bool: True if deleted successfully

        Raises:
            NotFoundException: If example not found
        """
        # Check if example exists
        await self.get_by_id(example_id)

        result = await self.collection.delete_one({"id": example_id})
        return result.deleted_count > 0
