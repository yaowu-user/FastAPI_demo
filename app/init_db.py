from app import models
from app.database import Base, engine



def main():
    """"根据已经注册的模型，在数据库自动创建表"""
    print("开始执行创建表的脚本")

    Base.metadata.create_all(bind=engine)
    print("相关的表已经创建成功")


if __name__ == "__main__":
    main()

  