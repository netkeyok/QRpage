# Используем официальный образ Python как базовый
FROM python:3.11.9-alpine3.19

# Установка переменных окружения для немедленного вывода логов в консоль
ENV PYTHONUNBUFFERED=1

# Установка необходимых инструментов и библиотек
RUN apk update \
    && apk add --no-cache curl gnupg unixodbc-dev g++ gcc make \
    && apk add --virtual .build-deps g++ gcc make

# Добавление ключа Microsoft GPG
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import -

# Скачивание и проверка пакетов
ARG architecture=amd64
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_$architecture.apk \
    && curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_$architecture.apk \
    && curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_$architecture.sig \
    && curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_$architecture.sig \
    && gpg --verify msodbcsql18_18.3.2.1-1_$architecture.sig msodbcsql18_18.3.2.1-1_$architecture.apk \
    && gpg --verify mssql-tools18_18.3.1.1-1_$architecture.sig mssql-tools18_18.3.1.1-1_$architecture.apk

# Установка пакетов
RUN apk add --allow-untrusted msodbcsql18_18.3.2.1-1_$architecture.apk \
    && apk add --allow-untrusted mssql-tools18_18.3.1.1-1_$architecture.apk

# Установка SQLAlchemy и pyodbc, копирование файлов проекта и установка зависимостей
COPY . .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Команды, выполняемые при запуске контейнера
CMD ["supervisord", "-c", "supervisord.conf"]