import json


from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import JSONResponse

from scrapper.dentalStallScrapper import scrap_dentalStall

app = FastAPI()
security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "admin" and credentials.password == "secret":
        return True
    return False


@app.get("/scrap")
async def scrap_all_data(background_tasks: BackgroundTasks, auth: bool = Depends(basic_auth)):
    if auth:
        background_tasks.add_task(scrap_dentalStall, 0)
        return JSONResponse(content="Process is running", status_code=200)
    return JSONResponse(content="Invalid Creds", status_code=401)

@app.get("/scrap/{pages}")
async def scrap_data(pages: int, background_tasks: BackgroundTasks, auth: bool = Depends(basic_auth)):
    if auth:
        background_tasks.add_task(scrap_dentalStall, pages)
        return "Process is running"
    return JSONResponse(content="Invalid Creds", status_code=401)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8033)

