from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/axios")
async def ax(request: Request):
    return templates.TemplateResponse("alp-axios.html", {"request": request})

@app.get('/alp')
async def alp(request: Request):
    return templates.TemplateResponse("alp.html", {"request": request})

@app.get('/x-on+hx-vals')
async def x_on_hx_vals(request: Request):
    return templates.TemplateResponse("x-on+hx-vals.html", {"request": request})

@app.get('/hx-enc')
async def hx_enc(request: Request):
    return templates.TemplateResponse("hx-enc.html", {"request": request})

@app.get('/hx-alp2')
async def hx_alp2(request: Request):
    return templates.TemplateResponse("hx-alp2.html", {"request": request})