"""
@description:自定义返回格式
"""
from fastapi import status
from fastapi.responses import JSONResponse


# 数据返回规则
def util_response(data=None, err=0, http_status=status.HTTP_200_OK, msg='ok'):
    if data is None:
        data = dict()
    if http_status == status.HTTP_200_OK:
        return JSONResponse({'err': err, 'msg': msg, 'data': data})
    else:
        return JSONResponse({'err': http_status, 'msg': msg}, status_code=http_status)
