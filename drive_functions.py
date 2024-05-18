import requests as req
import re
import json
import time

def countPages(file_uid):
    response = req.get(f"https://drive.google.com/file/d/{file_uid}/view",headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    })
    if response.status_code == 401:
        return {"success":False,"msg":"File is not publicly shared!","err":"FILE_NOT_ACCESSIBLE"}
    # print(response.text)
    mime = re.findall("\"docs-dm\":\"(.*)\",\"docs-sd",response.text)[0]
    if not mime=="application/pdf":
        return {"success":False,"msg":"Provided file is not a pdf file","err":"NOT_A_PDF"}
    uri = re.findall("(https:\/\/drive\.google\.com\/viewer[0-9]\/prod-[0-9][0-9]\/meta\?(.*))",response.text)
    meta_url = uri[0][0][0:uri[0][0].find("\"")].encode('utf-8').decode('unicode-escape')
    metadata = req.get(meta_url)
    title = re.findall("\<title\>(.*) - (.*)\<\/title\>",response.text)[0][0]
    return {
        "filename": title,
        "pages": json.loads(metadata.text[4::])['pages'],
        "mimetype": mime
    }


def countPages_light(file_uid,benchmark=False):
    benchmark_data={
        "pull_data": 0,
        "processing": 0,
        "regex": 0,
        "total": 0
    }
    pull_1_start = time.time()
    response = req.get(f"https://drive.google.com/file/d/{file_uid}/view",headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    })
    benchmark_data["pull_data"]+=time.time() - pull_1_start
    # print(response.text)
    regex_start = time.time()
    uri = re.findall("(https:\/\/drive\.google\.com\/viewer[0-9]\/prod-[0-9][0-9]\/meta\?(.*))",response.text)
    benchmark_data["regex"]+= time.time()-regex_start
    processing_start = time.time()
    meta_url = uri[0][0][0:uri[0][0].find("\"")].encode('utf-8').decode('unicode-escape')
    benchmark_data["processing"]+=time.time() - processing_start
    pull_2_start = time.time()
    metadata = req.get(meta_url)
    benchmark_data["pull_data"] += time.time() - pull_2_start
    benchmark_data["total"] = time.time() - pull_1_start
    res = {
        "pages": json.loads(metadata.text[4::])['pages']
    }
    if benchmark:
        res["benchmark"]=benchmark_data
    return res

def getFolderContents(folder_uid,benchmark=False):
    benchmark_data={
        "pull_data": 0,
        "regex": 0,
        "processing": 0,
        "total": 0
    }
    start = time.time()
    response = req.get(f"https://drive.google.com/drive/folders/{folder_uid}",headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    })
    if "Google Drive: Sign-in" in response.text:
        return {"success":False,"msg":"Provided Folder is not publicly shared","err":"FOLDER_NOT_ACCESSIBLE"}
    benchmark_data['pull_data']+=time.time()-start
    regex_start = time.time()
    folder_data = re.findall("window\['_DRIVE_ivd'\] = '(.*)'",response.text)
    try:
        title = re.findall("\<title\>(.*) - (.*)\<\/title\>",response.text)[0][0]
    except IndexError:
        print(response.text)
        title = None
    try:
        author = re.findall("(([a-z0-9A-Z\.]*)@gmail\.com)",response.text)[0][0]
    except IndexError:
        author = None
    folder_data = folder_data[0][0:folder_data[0].find("'")]
    raw_data = bytes(f"{folder_data}",'utf-8').decode('unicode-escape').encode().decode('unicode-escape')
    benchmark_data['regex']+=time.time()-regex_start
    processing_start = time.time()
    data_unprocessed = json.loads(raw_data)
    data_processed = []
    for i in data_unprocessed[0]:
        for j in i:
            if isinstance(j,list):
                i.remove(j)
        while True:
            try:
                i.remove(None)
            except ValueError:
                break
        data_processed.append({
            "uid": i[0],
            "filename": i[1],
            "mimetype": i[2],
            "link": i[-4],
            "size":i[9]
        })
    benchmark_data['processing']+=time.time()-processing_start
    res= {
        "success":True,
        "msg":"Success",
        "err":"NO_ERROR_ERROR",
        "name": title,
        "author": author,
        "totalContent":len(data_processed),
        "contents":data_processed
    }
    if benchmark:
        benchmark_data["total"] = time.time()-start
        res['benchmark']=benchmark_data
    return res


def countPagesAllPDF_Folder(folder_uid,benchmark=False):
    benchmark_data={
        "pull_data": 0,
        "regex": 0,
        "processing": 0,
        "page_count": 0,
        "total": 0
    }
    total_page = 0
    start = time.time()
    response = req.get(f"https://drive.google.com/drive/folders/{folder_uid}",headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    })
    if "Google Drive: Sign-in" in response.text:
        return {"suceess":False,"msg":"Provided folder is not publicly shared","err":"FOLDER_NOT_ACCESSIBLE"}
    benchmark_data['pull_data']+=time.time()-start
    regex_start = time.time()
    folder_data = re.findall("window\['_DRIVE_ivd'\] = '(.*)'",response.text)
    try:
        title = re.findall("\<title\>(.*) - (.*)\<\/title\>",response.text)[0][0]
    except IndexError:
        print(response.text)
        title = None
    try:
        author = re.findall("(([a-z0-9A-Z\.]*)@gmail\.com)",response.text)[0][0]
    except IndexError:
        author = None
    folder_data = folder_data[0][0:folder_data[0].find("'")]
    raw_data = bytes(f"{folder_data}",'utf-8').decode('unicode-escape').encode().decode('unicode-escape')
    benchmark_data['regex']+=time.time()-regex_start
    processing_start = time.time()
    data_unprocessed = json.loads(raw_data)
    data_processed = []
    for i in data_unprocessed[0]:
        for j in i:
            if isinstance(j,list):
                i.remove(j)
        while True:
            try:
                i.remove(None)
            except ValueError:
                break
        if i[2]=="application/pdf":
            pagecount_start = time.time()
            page_count_inf = countPages_light(i[0],benchmark=True)
            benchmark_data["page_count"]+=time.time() - pagecount_start
            total_page+=page_count_inf["pages"]
            benchmark_data["pull_data"]+=page_count_inf["benchmark"]["pull_data"]
            benchmark_data["regex"]+=page_count_inf["benchmark"]["regex"]
            benchmark_data["processing"]+=page_count_inf["benchmark"]["processing"]
            if benchmark:
                data_processed.append({
                    "uid": i[0],
                    "filename": i[1],
                    "mimetype": i[2],
                    "link": i[-4],
                    "size":i[9],
                    "pages": page_count_inf["pages"],
                    "benchmark":page_count_inf["benchmark"]
                })
            else:
                data_processed.append({
                    "uid": i[0],
                    "filename": i[1],
                    "mimetype": i[2],
                    "link": i[-4],
                    "size":i[9],
                    "pages": page_count_inf["pages"]
                })
        else:
            data_processed.append({
                "uid": i[0],
                "filename": i[1],
                "mimetype": i[2],
                "link": i[-4],
                "size":i[9]
            })
    benchmark_data['processing']+=time.time()-processing_start
    res= {
        "success": True,
        "msg": "Success",
        "err": "NO_ERROR_ERROR",
        "name": title,
        "author": author,
        "totalContent":len(data_processed),
        "contents":data_processed,
        "totalPages":total_page
    }
    if benchmark:
        benchmark_data["total"] = time.time()-start
        res['benchmark']=benchmark_data
    return res

if __name__ == "__main__":
    # pages = countPages("1wo1BSBNKfLDhDBF4ZHIigkQQQfm3pxg3")
    # print(pages)
    
    contents = getFolderContents("1mURYosXIDbqSzDYlnlqRtoKJzbv1KJ5J")
    print(json.dumps(contents,indent=2,ensure_ascii=False))