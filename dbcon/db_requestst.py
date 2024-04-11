from dbcon.egais_model import ConnectTap, ConnectTapSpec, Utms
from dbcon.config import session
from dbcon.egais_model import SMCardsOrange
from sqlalchemy import select, and_, desc


def request_docs(date_start=None, date_end=None, doc_id=None, orgid=None):
    with session as s:
        if doc_id:
            request = (
                select(
                    ConnectTapSpec.BaseId,
                    ConnectTapSpec.Mark,
                    ConnectTapSpec.ExpDay,
                    ConnectTap.DocDate,
                    ConnectTap.OrgId
                )
                .join(ConnectTap, ConnectTapSpec.BaseId == ConnectTap.id)
                .where(
                    and_(
                        ConnectTap.Status == 1,
                        ConnectTap.id == doc_id,
                    )
                )
            )
        elif date_start and date_end:
            request = (
                select(ConnectTapSpec.BaseId,
                       ConnectTapSpec.Mark,
                       ConnectTapSpec.ExpDay,
                       ConnectTap.DocDate
                       )
                .join(ConnectTap,
                      ConnectTapSpec.BaseId == ConnectTap.id)
                .where(
                    and_(
                        ConnectTap.Status == 1,
                        ConnectTap.DocDate.between(date_start, date_end),
                        ConnectTap.OrgId == orgid,
                    )
                ).order_by(ConnectTapSpec.BaseId)
            )
        else:
            request = (
                select(
                    ConnectTapSpec.BaseId,
                )
                .join(ConnectTap, ConnectTapSpec.BaseId == ConnectTap.id)
                .where(
                    and_(
                        ConnectTap.Status == 1,
                        ConnectTap.OrgId == orgid
                    )
                )
                .order_by(desc(ConnectTapSpec.BaseId))
                .limit(1)  # Ограничиваем результат одной записью с максимальным BaseId
            )

        # Получение результатов
        results = s.execute(request).all()

        return results


# def sync_barcodes():
#     # Очистка таблицы SMCardsOrange
#     try:
#         sessionMssql.query(SMCardsOrange).delete(synchronize_session=False)
#         sessionMssql.commit()
#     except IntegrityError as e:
#         print(f"Ошибка целостности при очистке таблицы SMCardsOrange: {e}")
#         sessionMssql.rollback()
#     except InvalidRequestError as e:
#         print(f"Неверный запрос при очистке таблицы SMCardsOrange: {e}")
#         sessionMssql.rollback()
#
#     # Формирование запроса для получения данных
#     SMrequest = (
#         select(SMCard.article, SMCard.shortname, SMStoreUnits.barcode)
#         .join(SMStoreUnits, SMCard.article == SMStoreUnits.article)
#         .where(
#             and_(
#                 SMCard.idclass.in_(
#                     select(SACardClass.id).where(SACardClass.tree.like('36.%'))
#                 ),
#                 SMStoreUnits.barcodetype == 7
#             )
#         )
#     )
#
#     # Получение данных из Oracle
#     SMresults = sessionOracle.execute(SMrequest).all()
#     for data in SMresults:
#         print(data)
#
#     # Вставка данных в таблицу SMCardsOrange
#     for article, shortname, barcode in SMresults:
#         new_card = SMCardsOrange(ARTICLE=article, SHORTNAME=shortname, BARCODE=barcode)
#         sessionMssql.add(new_card)
#
#     # Сохранение изменений в базе данных
#     try:
#         sessionMssql.commit()
#     except IntegrityError as e:
#         print(f"Ошибка целостности при вставке данных: {e}")
#         sessionMssql.rollback()
#     except InvalidRequestError as e:
#         print(f"Неверный запрос при вставке данных: {e}")
#         sessionMssql.rollback()
#
#     # Закрытие сессий
#     sessionMssql.close()
#     sessionOracle.close()
#
#     print('Complete')


def get_card(shkode):
    request = (
        select(SMCardsOrange.SHORTNAME).where(SMCardsOrange.BARCODE == shkode)
    )
    result = session.execute(request).scalar()
    return result


def organization_list():
    with session as s:
        org_list = (select(Utms.Id, Utms.Comment))
        result = s.execute(org_list)
        dict_iterator = result.mappings()
        return list(dict_iterator)


def org_name(id):
    with session as s:
        org = (select(Utms.Comment).
               where(Utms.Id == id))
        result = s.execute(org).fetchone()
    return result[0]


if __name__ == '__main__':
    pass
