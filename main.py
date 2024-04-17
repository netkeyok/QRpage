from fastapi import FastAPI
from dbcon.db_requestst import organization_list
from functions import send_docs_ids, check_doc_status

app = FastAPI()


@app.get("/orgs")
async def org_list():
    items = organization_list()
    return items


@app.get("/send/")
async def send_doc(doc_id: int):
    send_docs_ids(doc_id)
    status = 'Ok'
    return status


@app.get("/check/")
async def check():
    resilt = check_doc_status()
    return resilt
