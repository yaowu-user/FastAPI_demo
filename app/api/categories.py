from anyio import Path
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.common.response import Response
from app.schemas.category import CategoryRequest, CategoryResponse, CategoryStatisticResponse
from app.services import category_service
from typing import Annotated



router = APIRouter(prefix="/categories", tags=["分类相关的接口"])


@router.post("", response_model=Response)
def create_category(payload: CategoryRequest, db: Session = Depends(get_db)):
    return Response.success(
        data=CategoryResponse.model_validate(
            category_service.create_category(db, payload)
        )
    )

@router.patch("/{category_id}", response_model=Response)
def patch_category(
    payload: CategoryRequest,category_id: Annotated[int, Path(...,gt=0)], db: Annotated[Session, Depends(get_db)],
):
    return Response.success(
        data=CategoryResponse.model_validate(
            category_service.update_category(db, payload, category_id)
        )
    )


@router.delete("/{category_id}", response_model=Response)
def delete_category(
    category_id: Annotated[int, Path(...,gt=0)], db: Annotated[Session, Depends(get_db)],
):
    category_service.delete_category(db, category_id)
    return Response.success()

@router.get("",response_model=Response)
def read_categories(db: Annotated[Session, Depends(get_db)]):
    return Response.success(
        data=[
            CategoryResponse.model_validate(item)
            for item in category_service.get_categories(db)  # model
        ]  # [CategoryResponse1, CategoryResponse2, ...]
    )


@router.get("/statistics",response_model=Response, summary="统计分类商品数量")
def read_categories(db: Annotated[Session, Depends(get_db)]):
    return Response.success(
        data=[
            CategoryStatisticResponse.model_validate(item)
            for item in category_service.get_category_statistics(db)
        ]
    )
