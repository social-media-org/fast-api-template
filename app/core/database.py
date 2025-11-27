"""Database connection management."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

# MongoDB client (will be initialized in lifespan)
mongo_client: AsyncIOMotorClient | None = None


def get_database() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance.

    Returns:
        AsyncIOMotorDatabase: MongoDB database instance

    Raises:
        RuntimeError: If database is not initialized
    """
    if mongo_client is None:
        raise RuntimeError("Database not initialized")
    return mongo_client[settings.mongodb_database]
