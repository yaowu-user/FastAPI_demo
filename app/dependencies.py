from app.database import SessionLocal


def get_db():
    """为一次请求提供 Session,使用结束后关闭。"""
    with SessionLocal() as db:
        yield db