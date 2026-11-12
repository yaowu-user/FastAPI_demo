import logging

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessError
from app.models import Category
from app.models.product import Product
from app.schemas.category import CategoryRequest

logger = logging.getLogger(__name__)

# 请求1：查询 “饮料” -> 饮料没有 -> 写进去 新增 "饮料"
# 请求2：查询 “饮料” -> 饮料没有 —> 新增 "饮料"（报错了）


def create_category(db: Session, payload: CategoryRequest) -> Category:


    # statement = select(Category.id).where(Category.name == name)
    # exsist_id = db.scalar(statement)
    # if exsist_id is not None:
    #     raise BusinessError("分类名称已存在", code=409)

    category = Category(name=payload.name)
    try:
        db.add(category)
        db.commit()
        db.refresh(category)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("新增分类数据库操作失败")
        # 分类名有唯一约束，仅 MySQL 1062 表示这里的重名冲突。
        if isinstance(exc, IntegrityError) and exc.orig.args[0] == 1062:
            raise BusinessError("分类名称已存在", code=409) from exc
        raise

    return category

def update_category(db: Session, payload: CategoryRequest,category_id: int) -> Category:
    category = db.get(Category, category_id)
    if not category:
        raise BusinessError(message = "分类不存在", code=404)
    category.name = payload.name
    try:
        db.commit()
        db.refresh(category)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("修改分类数据库操作失败")
        # 分类名有唯一约束，仅 MySQL 1062 表示这里的重名冲突。
        if isinstance(exc, IntegrityError) and exc.orig.args[0] == 1062:
            raise BusinessError("分类名称已存在", code=409) from exc
        raise

    return category

def delete_category(db: Session, category_id: int):
    category = db.get(Category, category_id)
    if category is None:
        raise BusinessError(message="分类不存在", code=404)
    product_count = db.scalar(
        select(func.count(Product.id)).where(Product.category_id == category_id)
    )
    if product_count > 0:
        raise BusinessError(message="分类下有其他商品，不能删除分类", code=409)
    try:
        db.delete(category)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("删除分类数据库操作失败")
        raise

def get_categories(db: Session):
    """查询所有的商品分类"""
    try:
        statement = select(Category).order_by(Category.id.desc())
        return db.scalars(statement).all()
    except SQLAlchemyError as exc:
        logger.exception("查询分类列表失败")
        raise BusinessError("查询分类失败，请稍后重试", code=500) from exc

def get_category_statistics(db: Session):
    """查询商品分类商品数量统计，包含没有商品的分类。"""
    stmt = select(Category.id, Category.name, func.count(Product.id).label("product_count")
    ).outerjoin(Product, Product.category_id == Category.id).group_by(Category.id, Category.name).order_by(Category.id.asc())
    rows = db.execute(stmt).all()
    return [
        {"id": category_id, "name": category_name, "product_count": product_count} 
        for category_id, category_name, product_count in rows
    ]