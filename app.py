from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from drive_functions import countPages,getFolderContents,countPagesAllPDF_Folder

app = FastAPI()

@app.get("/countPdfPages/{file_uid}")
def serveFileDetails(file_uid:str):
    return countPages(file_uid=file_uid)

@app.get("/getFolderContents/{folder_uid}")
def serveFolderDetails(folder_uid:str, depth: Union[int,None]=1, benchmark: Union[bool,None]=False, count_pdf_pages: Union[bool,None]=False):
    if count_pdf_pages:
        return {"response":countPagesAllPDF_Folder(folder_uid,benchmark),"depth":depth}
    return {"response":getFolderContents(folder_uid,benchmark),"depth":depth}