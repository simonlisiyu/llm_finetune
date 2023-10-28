FROM cuda_python:3.9.13-gpu
LABEL org.opencontainers.image.authors="otter202@gmail.com"

WORKDIR /app

COPY requirements.txt .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

COPY . .

CMD ["bash", "scripts/init.sh"]



