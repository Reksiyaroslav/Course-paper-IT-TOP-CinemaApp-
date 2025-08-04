FROM python:3.12-slim
WORKDIR /app
COPY  . /app
RUN  pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 90 
CMD ["litestar","run","--host","0.0.0.0","--port","90"]