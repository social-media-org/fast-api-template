"""Example endpoints for CRUD operations."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_example_service
from app.models.example_model import (
    ExampleCreate,
    ExampleResponse,
    ExampleUpdate,
)
from app.services.example_service import ExampleService

router = APIRouter()


@router.post(
    "",
    response_model=ExampleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new example",
    description="Create a new example with the provided data.",
)
async def create_example(
    example: ExampleCreate,
    service: Annotated[ExampleService, Depends(get_example_service)],
) -> ExampleResponse:
    """Create a new example.

    Args:
        example: Example data to create
        service: Example service instance (injected)

    Returns:
        ExampleResponse: Created example
    """
    return await service.create_example(example)


@router.get(
    "/{example_id}",
    response_model=ExampleResponse,
    summary="Get example by ID",
    description="Retrieve a single example by its unique identifier.",
)
async def get_example(
    example_id: str,
    service: Annotated[ExampleService, Depends(get_example_service)],
) -> ExampleResponse:
    """Get example by ID.

    Args:
        example_id: Example UUID
        service: Example service instance (injected)

    Returns:
        ExampleResponse: Example data
    """
    return await service.get_example_by_id(example_id)


@router.get(
    "",
    response_model=List[ExampleResponse],
    summary="List all examples",
    description="Retrieve a paginated list of all examples.",
)
async def list_examples(
    skip: Annotated[int, Query(ge=0, description="Number of records to skip")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Maximum number of records")] = 100,
    service: Annotated[ExampleService, Depends(get_example_service)],
) -> List[ExampleResponse]:
    """List all examples with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Example service instance (injected)

    Returns:
        List[ExampleResponse]: List of examples
    """
    return await service.list_examples(skip=skip, limit=limit)


@router.put(
    "/{example_id}",
    response_model=ExampleResponse,
    summary="Update example",
    description="Update an existing example with partial or complete data.",
)
async def update_example(
    example_id: str,
    example: ExampleUpdate,
    service: Annotated[ExampleService, Depends(get_example_service)],
) -> ExampleResponse:
    """Update an existing example.

    Args:
        example_id: Example UUID
        example: Updated example data
        service: Example service instance (injected)

    Returns:
        ExampleResponse: Updated example
    """
    return await service.update_example(example_id, example)


@router.delete(
    "/{example_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete example",
    description="Delete an example by its unique identifier.",
)
async def delete_example(
    example_id: str,
    service: Annotated[ExampleService, Depends(get_example_service)],
) -> None:
    """Delete an example.

    Args:
        example_id: Example UUID
        service: Example service instance (injected)
    """
    await service.delete_example(example_id)
