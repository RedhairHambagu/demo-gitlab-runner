FROM python:3.11-slim

# 配置 pip 使用国内镜像源（清华大学镜像）
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 18000
CMD ["gunicorn", "--bind", "0.0.0.0:18000", "app:app"]
