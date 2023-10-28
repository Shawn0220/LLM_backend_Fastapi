# LLM-Chat-Backend

LLM-Chat后端服务

# docker 部署

```
docker build -t reg.hdec.com/pdc/tianji-backend:v1 .
docker push reg.hdec.com/pdc/tianji-backend:v1
```

在aiuser机器上编译, Jenkins上报了奇怪的错误,可能有各种原因
此次基础镜像是重新编译的，python版本，cuda版本都比较新，也是在aiuser机器上编译的

## 环境变量

source environment

## 启动命令

python -m uvicorn main:app --port=8002 --host=0.0.0.0 --reload