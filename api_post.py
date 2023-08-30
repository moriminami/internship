from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from basic_auth import verify_from_api
import llm_process
import webbrowser

app = FastAPI()

# CORS設定
origins = [
    'http://localhost',
    'http://localhost:8000',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンからのアクセスを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 認証状態を管理する変数
authrized_status = 0

class Input(BaseModel):
    question: str
    model: str

class Output(BaseModel):
    answer: str

@app.post("/process/")
async def main(input_data: Input):
    global authrized_status

    # 入力データを取得
    question = input_data.question
    model = input_data.model

    if authrized_status == 0:
        answer = "ログインしてください"
    else:
        # モデルの設定
        print(f'モデル：{model}')
        if model == "llama2":
            answer = llm_process.llama2(question)
        elif model == "line_llm":
            answer = llm_process.line_llm(question)
        elif model == "東大_llm":
            answer = llm_process.toudai_llm(question)

    output_data = Output(answer=answer)
    return output_data


#ユーザーは'minami'、パスワードは'mori'、どちらも環境変数で設定
@app.get("/")
async def root(_=Depends(verify_from_api)):
    html_file_path = r"C:\Users\m_mori\Desktop\llm_chat\login.html"  # 表示したいHTMLファイルのパスを指定
    webbrowser.open(html_file_path)

    global authrized_status
    authrized_status = 1

    return {'authrized': 'OK'}
