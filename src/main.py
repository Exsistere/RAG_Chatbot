from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from core import rag
from model import llm
from Prompt import llm_prompt
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name= "static")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
UPLOAD_DIR = os.path.join(PROJECT_DIR, "Data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)




@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

#file upload
@app.post("/upload", response_class=HTMLResponse)
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    rag.embed_pdf(file_path)
#context retrival    
@app.post("/query", response_class=HTMLResponse)
async def query_context(query: str = Form(...)):
    vector_DB_data = rag.query_retrival(query)
    template = llm_prompt.load_prompt_template()
    system_prompt, user_prompt = llm_prompt.render_prompt(template, query, str(vector_DB_data["documents"]))
    reponse = llm.ask_gemini(user_prompt, system_prompt)
    return f"""
        <div class="context_info">
            <b> Retrieved chunks: </b>
            {vector_DB_data['documents']}
            <br>
        </div>
        
        <div class="prompt">
            <b>System Prompt:  </b>
            {system_prompt}
            <br>
            <b> User Prompt: </b>
            {user_prompt}
        </div>

        <div>
            <b>gemini response</b>
            <br>
            {reponse.text}
        </div>
        """