from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import user_router
from backend.routers import route_router
from backend.core.database import engine
from backend.models import Base
from fastapi.routing import APIRoute

# 创建 FastAPI 实例
app = FastAPI()
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名的跨域请求，生产环境中最好指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法，如 GET, POST, PUT, DELETE
    allow_headers=["*"],  # 允许所有 HTTP 请求头
)
Base.metadata.create_all(bind=engine)

# 搭载
app.include_router(user_router.router)
app.include_router(route_router.router)

# 打印所有路由信息
@app.on_event("startup")
async def print_routes():
    print("当前注册的所有路由：")
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"{route.path}  -->  {', '.join(route.methods)}")

@app.get("/")
def read_root():
    return {"message": "成功"}
