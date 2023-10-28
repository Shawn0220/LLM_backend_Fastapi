"""
@description:主模块
"""
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量

load_dotenv()

import os
import logging
from logging import handlers
import uvicorn
from fastapi import FastAPI, Request, status, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi_pagination import add_pagination
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from apps.chat.router import router as user_router, websocket_llm_handler
from apps.chat.admin_router import router as admin_router
from utils.custom_response import util_response
from utils.custom_config import BASE_DIR


ENV = os.environ.get('ENV_PROFILE')


# 主程序
app = FastAPI(
    title="FastAPI结构示例",  # 文档标题
    description="使用FastAPI实现基础的用户验证，权限管理，增删改查，文件上传下载等功能. 🚀",  # 文档简介
    version="0.0.1",  # 文档版本号
    docs_url=None, redoc_url=None,  # 配置离线文档
)


# 配置日志记录【记录 uvicorn 的日志】
@app.on_event("startup")
async def startup_event():
    log_path = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    format_str = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  # 设置日志格式
    logger = logging.getLogger("uvicorn.access")  # 获取日志对象
    # sh = logging.StreamHandler()  # 往屏幕上输出
    rh = handlers.RotatingFileHandler("logs/uvicorn.log", maxBytes=100 * 1024, backupCount=7, encoding='utf-8')  # 写入文件
    # sh.setFormatter(format_str)  # 指定格式
    rh.setFormatter(format_str)  # 指定格式
    # logger.addHandler(sh)
    logger.addHandler(rh)


# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 允许跨域请求的源列表。
    allow_credentials=True,  # 指示跨域请求支持 cookies。
    allow_methods=["*"],  # 允许跨域请求的 HTTP 方法列表。
    allow_headers=["*"],  # 允许跨域请求的 HTTP 请求头列表。
)


# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/media", StaticFiles(directory="media"), name="media")


# 离线文档配置-由于资源文档经常请求不到，这里搞离线文档
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/doc/swagger-ui-bundle.js",
        swagger_css_url="/static/doc/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


# 覆盖 HTTPException 错误处理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return util_response(http_status=exc.status_code, msg=str(exc.detail))


# 覆盖默认异常处理器[RequestValidationError是 Pydantic 的ValidationError的子类。]
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return util_response(http_status=status.HTTP_400_BAD_REQUEST, msg=str(exc))


# todo 这里先这样定义全局异常返回，待优化
@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = util_response(http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             msg='Internal server error')
    # finally:
    #     return response
    # if ENV=='dev':
    #     try:
    #         response = await call_next(request)
    #     except Exception as e:
    #         response = util_response(http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                              msg=f'Internal server error:{str(e)}')
    #         # msg=f'Internal server error:{str(e)}')
    #         logging.error(str(e))
    #         print(str(e))
    # elif ENV=='prod':
    #     response = await call_next(request)
    response = await call_next(request)
    return response

# 路由注册
app.include_router(user_router)
app.include_router(admin_router)

@app.get("/", tags=['测试'], deprecated=True)
async def root():
    return util_response(data='fast_api!')

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, x_current_user_id: int):
    await websocket_llm_handler(websocket, x_current_user_id)

add_pagination(app)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8002/ws/chat`);
            ws.onopen = function (event) {
                // 设置请求头
                ws.setRequestHeader('X-Current-User_Id', 1231);
            };
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/ws-html")
async def get():
    return HTMLResponse(html)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8002, reload=True, log_config='uvicorn_config.json')  # 可以直接运行此脚本
