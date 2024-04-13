from datetime import datetime, timedelta

from dbcon.egais_model import ConnectTap, ConnectTapSpec, Utms, ConnectTapLog
from dbcon.config import session
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


def check_docs(doc_id):
    with session as s:
        request = (
            select(ConnectTapLog.id,
                   ConnectTapLog.Status,
                   ConnectTapLog.Error,
                   ConnectTapLog.DocDateSend)
        ).where(ConnectTapLog.id == doc_id
                ).order_by(desc(ConnectTapLog.DocDateSend)
                           ).limit(1)
    result = s.execute(request).all()
    return result


def update_doc_log(doc_id, error=None):
    with session as s:
        if error:
            new_log = ConnectTapLog(
                id=doc_id,
                DocDateSend=datetime.now(),
                Status=1,
                Error=error
            )
        else:
            new_log = ConnectTapLog(
                id=doc_id,
                DocDateSend=datetime.now(),
                Status=2,
                Error=None
            )
        s.merge(new_log)
        s.commit()


def check_doc_log(doc_id):
    with session as s:
        request = (
            select(ConnectTapLog.id,
                   ConnectTapLog.Status,
                   ConnectTapLog.Error,
                   ConnectTapLog.DocDateSend)
        ).where(ConnectTapLog.id == doc_id
                ).order_by(desc(ConnectTapLog.DocDateSend)
                           ).limit(1)
    result = s.execute(request).all()
    if result:
        return result
    else:
        return None


if __name__ == '__main__':
    date_now = datetime.now()
    date_ago = date_now - timedelta(days=2)

    data = request_docs(date_start=date_ago, date_end=date_now, orgid=27)
    for d in data:
        print(d)
