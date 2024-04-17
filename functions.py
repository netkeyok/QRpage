import os
import sys


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode
import smtplib
from email.message import EmailMessage
from dbcon.config import server_email, redis_conn
from email_list import mail_dict
from datetime import datetime, timedelta
from dbcon.db_requestst import request_docs, organization_list, org_name, update_doc_log, check_doc_log
from api_request.request_to_sm import get_article_name
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

orgs = organization_list()

# Путь до папки темп
path = os.path.join(sys.path[0], "temp")


def send_email(shop, doc, shcode=None, file_path=None, card_name=None):
    recipient_email = ''
    if shop in mail_dict:
        recipient_email = mail_dict[shop]
        # print(shop)
    else:
        print(shop)
        print("Адрес не найден")

    try:
        msg = EmailMessage()
        msg['From'] = 'qr@local'
        msg['To'] = recipient_email

        if file_path and card_name:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                msg_text = f'QR коды {card_name} К документу {doc}'
                msg['Subject'] = msg_text
                msg.set_content(msg_text)
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_path)
                update_doc_log(doc_id=doc)
        else:
            error_text = 'Штрихкод не найден'
            msg = MIMEMultipart('alternative')
            msg['From'] = 'qr@local'
            msg['To'] = recipient_email
            msg['Subject'] = error_text

            # HTML-версия письма
            html_content = f"""
            <html>
            <body>
            <p>Штрихкод из марки документа <span style="color:red">{doc}</span> отсутствует в базе супермаг,<br>
            передайте данный штрихкод <span style="color:red">{shcode}</span> старшему оператору,<br>
            чтобы он добавил его в базу данных Супермаг.</p>
            </body>
            </html>
            """
            # Добавляем HTML-версию в сообщение
            msg.attach(MIMEText(html_content, 'html'))
            update_doc_log(doc_id=doc, error=error_text)
        with smtplib.SMTP(server_email, 25) as smtp:
            smtp.send_message(msg)
            print('Email sent successfully')

    except Exception as e:
        error_text = f'Failed to send email: {e}'
        update_doc_log(doc_id=doc, error=f'Failed to send email: {e}')
        print(error_text)
    if file_path is not None and os.path.exists(file_path):
        os.remove(file_path)


# Функция создания pdf файла с QR
def create_pdf_with_images(image_path, output_pdf_path, caption, title):
    # Регистрация шрифта TrueType
    pdfmetrics.registerFont(TTFont('courier', 'courier.ttf'))  # Укажите путь к файлу шрифта
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4
    image_width = (width - 20 * mm) / 5
    image_height = height / 5
    left_margin = 20 * mm
    caption_height = 8  # Высота шрифта для подписи

    # Установка шрифта для заголовка и текста
    c.setFont('courier', 30)  # Шрифт для заголовка
    c.drawString(left_margin, height - 20 * mm, title)  # Размещение заголовка

    # Установка шрифта для текста
    c.setFont('courier', 6)  # Используйте зарегистрированный шрифт

    for index, (row, col) in enumerate([(r, c) for r in range(4) for c in range(5)]):
        x = col * image_width + left_margin
        y = height - (row + 1) * image_height
        # Рисуем изображение
        c.drawImage(image_path, x, y, width=40, height=40, preserveAspectRatio=True)
        # Подпись над изображением
        c.drawString(x - 5, y + 50, caption[0])
        c.drawString(x - 5, y + 45, caption[1])
        c.drawString(x - 5, y + 40, caption[2])
        # Первая строка подписи под изображением
        c.drawString(x, y - caption_height, caption[3])
        # Вторая строка подписи под изображением
        c.drawString(x, y - 2 * (caption_height), caption[4])
        # Вертикальная подпись перед изображением
        c.saveState()  # Сохраняем состояние канвы, чтобы вернуться к нему после поворота
        c.translate(x - 10, y + 46)  # Перемещаем начало координат к месту начала текста
        c.rotate(90)  # Поворачиваем канву на 90 градусов
        c.drawString(-60, 0, caption[5])  # Рисуем текст в новых координатах
        c.restoreState()  # Восстанавливаем состояние канвы

    c.save()


# Создание изображения QR кода
def create_qr(gs1, expdate, shop, doc_id):
    shop_name = f'Магазин {shop}'
    name = get_article_name(gs1)

    file_image = f'{shop_name}_{doc_id}_qr_code.png'
    temp_image = os.path.join(path, file_image)

    pdf_writer = f'{shop_name}_{doc_id}_.pdf'

    symbol = chr(29)
    gs2 = f"""{gs1[:25]}{symbol}{gs1[-6:]}"""
    # Получение шк из марки
    shcode = gs1[3:16]

    # кол-во разлитого напитка
    volume = '01500'

    # Формируем код согласно шаблону УКМ4
    qr_data = fr'{gs2}3353{volume}'
    text = 'Не является маркой!'

    qr_img = qrcode.make(qr_data)
    qr_img.save(temp_image)
    file_pdf = os.path.join(path, pdf_writer)
    captions = ''
    if name:
        captions = [name[:17], name[17:35], name[35:], shcode, expdate, text]
        create_pdf_with_images(temp_image, file_pdf, captions, shop_name)
        send_email(file_path=file_pdf, shop=shop, doc=doc_id, card_name=name)
        if temp_image is not None and os.path.exists(temp_image):
            os.remove(temp_image)

    else:
        send_email(shop=shop, doc=doc_id, shcode=shcode)
        # captions = ['Не печатать!'] * 6
        # captions[3] = shcode
        # pdf_writer = f'{shop_name}_{doc_id}_Не печатать.pdf'
    # Генерация QR-кода

    # qr_img = qrcode.make(qr_data)
    # qr_img.save(temp_image)


def send_docs_dates():
    # Текущее время
    current_time = datetime.now()
    print("Текущее время:", current_time)

    day = 10
    # 14 дней назад
    days_ago = current_time - timedelta(days=day)
    print(f"{day} дней назад:", days_ago)

    for i in orgs:
        if i:
            org_name = i['Comment']
            org_id = i['Id']
            docs = request_docs(date_start=days_ago, date_end=current_time, orgid=i['Id'])
            for doc_id, mark, expdays, doc_date in docs:
                expday = doc_date + timedelta(expdays)
                create_qr(mark, expday.strftime('%d.%m.%Y'), org_name, doc_id, org_id)


def send_docs_ids(doc_id):
    docs = request_docs(doc_id=doc_id)
    for doc_id, mark, expdays, doc_date, org in docs:
        expday = doc_date + timedelta(expdays)
        # print(doc_id, mark, expday.strftime('%d.%m.%Y'), org_name(org), org)
        create_qr(gs1=mark, expdate=expday.strftime('%d.%m.%Y'), shop=org_name(org), doc_id=doc_id, org_id=org)
    return f'{doc_id} is send'


def check_doc_status():
    date_now = datetime.now()
    date_ago = date_now - timedelta(days=4)
    added = []
    resend = []
    waiting = []
    for i in orgs:
        org = i['Id']
        data = request_docs(date_start=date_ago, date_end=date_now, orgid=org)
        for d in data:
            doc_id = d[0]
            print(f'Проверка документа: {doc_id}')
            result_check = check_doc_log(doc_id)
            if result_check is None:
                send_docs_ids(doc_id)
                added.append(doc_id)
            elif result_check[0][1] == 1:
                if get_article_name(d[1]):
                    send_docs_ids(doc_id)
                    resend.append(doc_id)
                else:
                    waiting.append(doc_id)
    return {
        'docs_add': added,
        'docs_resend': resend,
        'waiting_docs': waiting
    }


if __name__ == '__main__':
    # send_docs_ids(302)
    # create_pdf_with_text('output.pdf', '123456', '7890123456789')
    # send_email("Апельсин 18", org_id=99, doc=585, shcode='7890123456789')
    # send_email("Апельсин 18", org_id=99, doc=585, shcode='7890123456789')
    check_doc_status()
