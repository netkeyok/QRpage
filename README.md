Временный мини сервер для утилиты печати пивных QR кодов

# Для запуска:
docker build . --tag qr_page --no-cache && docker run --name qr_page -p 8082:8082 --env-file ./.env qr_page

