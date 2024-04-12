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
from dbcon.db_requestst import request_docs, organization_list, org_name
from api_request.request_to_sm import get_article_name
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

orgs = organization_list()

# Путь до папки темп
path = os.path.join(sys.path[0], "temp")


# Функция отправки файла на эл почту компании
# def send_email(file_path, shop, doc, art_name, org_id):
#     recipient_email = ''
#     if shop in mail_dict:
#
#         recipient_email = mail_dict[shop]
#     else:
#         print("Адрес не найден")
#
#     try:
#         with open(file_path, 'rb') as file:
#             file_data = file.read()
#         msg_text = f'QR коды {art_name} К документу {doc}'
#         msg = EmailMessage()
#         msg['From'] = 'qr@local'
#         msg['To'] = recipient_email
#         msg['Subject'] = msg_text
#         msg.set_content(msg_text)
#         msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_path)
#
#         with smtplib.SMTP(server_email, 25) as smtp:
#             smtp.send_message(msg)
#             print('Email sent successfully')
#             redis_conn.set(org_id, doc)
#
#     except Exception as e:
#         print(f'Failed to send email: {e}')

def send_email(shop, doc, org_id, shcode=None, file_path=None, art_name=None):
    recipient_email = ''
    if shop in mail_dict:
        recipient_email = mail_dict[shop]
    else:
        print("Адрес не найден")

    try:
        msg = EmailMessage()
        msg['From'] = 'qr@local'
        msg['To'] = recipient_email

        if file_path and art_name:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                msg_text = f'QR коды {art_name} К документу {doc}'
                msg['Subject'] = msg_text
                msg.set_content(msg_text)
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_path)
        else:
            msg = MIMEMultipart('alternative')
            msg['From'] = 'qr@local'
            msg['To'] = recipient_email
            msg['Subject'] = 'Штрихкод не найден'

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
        with smtplib.SMTP(server_email, 25) as smtp:
            smtp.send_message(msg)
            print('Email sent successfully')
            redis_conn.set(org_id, doc)

    except Exception as e:
        print(f'Failed to send email: {e}')


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


# def create_pdf_with_text(output_pdf_path, doc_id, shcode):
#     # Регистрация шрифта TrueType
#     pdfmetrics.registerFont(TTFont('courier', 'courier.ttf'))  # Укажите путь к файлу шрифта
#     c = canvas.Canvas(output_pdf_path, pagesize=A4)
#     width, height = A4
#     left_margin = 15 * mm
#
#     # Заголовок красным цветом
#     c.setFont('courier', 24)  # Размер шрифта для заголовка
#     c.setFillColor(red)
#     c.drawString(left_margin, height - 40 * mm, "Внимание!")
#
#     # Текст для вывода в PDF, разбитый на три строки
#     text_line1 = f"Штрихкод из марки документа {doc_id} отсутствует в базе супермаг,"
#     text_line2 = f"передайте данный штрихкод {shcode} старшему оператору,"
#     text_line3 = f"чтобы он добавил его в базу данных Супермаг"
#
#     # Установка шрифта для текста
#     c.setFont('courier', 14)  # Размер шрифта для текста
#     c.setFillColor(black)  # Возвращаем цвет текста к черному
#
#     # Размещение текста
#     c.drawString(left_margin, height - 60 * mm, text_line1)
#
#     # Выделение переменных красным цветом
#     c.setFillColor(red)
#     c.drawString(left_margin + c.stringWidth(text_line1[:text_line1.find(doc_id)]), height - 60 * mm, doc_id)
#     c.setFillColor(black)
#     c.drawString(left_margin + c.stringWidth(text_line1), height - 60 * mm,
#                  text_line1[text_line1.find(doc_id) + len(doc_id):])
#
#     c.drawString(left_margin, height - 70 * mm, text_line2)
#     c.setFillColor(red)
#     c.drawString(left_margin + c.stringWidth(text_line2[:text_line2.find(shcode)]), height - 70 * mm, shcode)
#     c.setFillColor(black)
#     c.drawString(left_margin + c.stringWidth(text_line2), height - 70 * mm,
#                  text_line2[text_line2.find(shcode) + len(shcode):])
#
#     c.drawString(left_margin, height - 80 * mm, text_line3)
#
#     c.save()


# Создание изображения QR кода
def create_qr(gs1, expdate, shop, doc_id, org_id):
    shop_name = f'Магазин {shop}'

    file_image = f'{shop_name}_{doc_id}_qr_code.png'
    temp_image = os.path.join(path, file_image)

    pdf_writer = f'{shop_name}_{doc_id}_.pdf'

    symbol = chr(29)
    gs2 = f"""{gs1[:25]}{symbol}{gs1[-6:]}"""
    # Получение шк из марки
    shcode = gs1[3:16]

    # кол-во разлитого напитка
    volume = '01500'
    name = get_article_name(shcode)
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
        send_email(file_pdf, shop, doc_id, name, org_id)

    else:
        send_email(shop=shop, org_id=org_id, doc=doc_id, shcode=shcode)
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
        print(doc_id, mark, expday.strftime('%d.%m.%Y'))
        create_qr(mark, expday.strftime('%d.%m.%Y'), org_name(org), doc_id, org)
    return f'{doc_id} is send'


def check_docs():
    print("start checking")
    res = None
    for i in orgs:
        org = i['Id']
        data = request_docs(orgid=org)
        result = redis_conn.get(org)
        if data and result:
            doc_id = data[0][0]
            int_result = int(result)
            if int_result != doc_id:
                send_docs_ids(doc_id)
                res = f'Document No. {doc_id} was sent'
            else:
                res = 'Nothing to send'
    print('End checking')
    return res


if __name__ == '__main__':
    # send_docs_ids(583)
    # create_pdf_with_text('output.pdf', '123456', '7890123456789')
    # send_email("Апельсин 18", org_id=99, doc=585, shcode='7890123456789')
    send_email("Апельсин 18", org_id=99, doc=585, shcode='7890123456789')
