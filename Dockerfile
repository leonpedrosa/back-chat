# docker build -t registry.lunioit.com/api_integracao_desktop:dev . && docker push registry.lunioit.com/api_integracao_desktop:dev
FROM alpine:3.18
ENV PYTHONUNBUFFERED 1
ENV TZ=America/Sao_Paulo
RUN apk update && apk add --no-cache tzdata curl python3 py3-pip gcc python3-dev postgresql-dev libc-dev file-dev && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt --no-cache-dir
CMD ["uvicorn","--bind=0.0.0.0:8021", "--workers=4", "--threads=4", "--worker-class=gthread", "--worker-tmp-dir=/dev/shm", "--log-level", "debug", "integracao_desktop.wsgi:application"]
