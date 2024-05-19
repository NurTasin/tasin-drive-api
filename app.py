from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from drive_functions import countPages,getFolderContents,countPagesAllPDF_Folder

app = FastAPI(title="Tasin's Unofficial Drive API",
              summary="""This API is created as a SaaS for parsing Google Drive's Webapp to get details about the destined file or folder""",
              description="""[Contribute on Github](https://github.com/NurTasin/tasin-drive-api)""",
              version="1.0.0(alpha)",
              docs_url="/",
              contact={
                  "name":"Nur Mahmud Tasin",
                  "url":"https://github.com/NurTasin",
                  "email":"bigtdevs@gmail.com"
              })

@app.get("/api/v1/countPdfPages/{file_uid}",
         name="Count PDF Page",
         description="Counts pages from a file ID of a pdf file.",
         response_description="""Response Structure looks like this
```json
{
    "success": true, // If the operation was successful or not
    "msg": "System generated Message", // Provides more data about the error (if occured)
    "err": "NO_ERROR_ERROR", //Short Code for that specific error [NO_ERROR_ERROR,FOLDER_NOT_ACCESSIBLE,FILE_NOT_ACCESSIBLE,NOT_A_PDF]
    "filename": "NAME OF THE FILE",
    "pages": 69, //Page count of that file
    "mimetype":"application/pdf" // MIME Type of the file
}""")
def serveFileDetails(file_uid:str,cache:Union[None,bool] = False):
    return countPages(file_uid=file_uid,cache=True)

@app.get("/api/v1/getFolderContents/{folder_uid}",
         name="get Folder Contents",
         description="Responds with the contents (file,folder) from a publicly shared Drive Folder",
         response_description="""This endpoint responds like
```json
{
    "success": true, // If the operation was successful or not
    "msg": "System generated Message", // Provides more data about the error (if occured)
    "err": "NO_ERROR_ERROR", //Short Code for that specific error [NO_ERROR_ERROR,FOLDER_NOT_ACCESSIBLE,FILE_NOT_ACCESSIBLE,NOT_A_PDF]
    "name": "Name of the folder", // null if unable to parse the name
    "author": "email address of the author", // null if unable to parse,
    "totalContent": 6 // Total ammount of elements (files and folders) present inside that folder
    "contents":[
        {
            "uid": "aouriguahgjhg", // File uid,
            "filename": "File name",
            "mimetype": "mimetype of the file",
            "size": 565654, // Size of the file (in bytes)
            "link": "https://drive.google.com/file/d/airhgurhg", // Drive link to that file
            "pages": 45 // total pages of the file (if mimetype == application/pdf and count_pdf_pages == true)
            "benchmark": {
                "pull_data": 1.000234, //Amount of total time spent to pull data from remote server (if benchmark==true)
                "regex": 0.0054, // Amount of total time spent to match regex patterns and get matches (if benchmark == true)
                "processing": 0.000154, //Amount of total time spent to precess data (if benchmark == true)
                "total": 1.00451 //Amount of total time spent to serve this response from getting response (if benchmark == true)
            }
        },
        ...
    ],
    "totalPages": 100, // Total pages of pdf documents found inside that folder (if count_pdf_pages==true)
    "benchmark": {
        "pull_data": 1.000234, //Amount of total time spent to pull data from remote server (if benchmark==true)
        "regex": 0.0054, // Amount of total time spent to match regex patterns and get matches (if benchmark == true)
        "processing": 0.000154, //Amount of total time spent to precess data (if benchmark == true)
        "total": 1.00451 //Amount of total time spent to serve this response from getting response (if benchmark == true)
    }
}
```""")
def serveFolderDetails(folder_uid:str, depth: Union[int,None]=1, benchmark: Union[bool,None]=False, count_pdf_pages: Union[bool,None]=False,cache: Union[bool,None] = True):
    if count_pdf_pages:
        return {"response":countPagesAllPDF_Folder(folder_uid,benchmark=benchmark,cache=cache),"depth":depth}
    return {"response":getFolderContents(folder_uid,benchmark=benchmark,cache=cache),"depth":depth}