from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar depois para segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    senha: str

def get_conn():
    return psycopg2.connect(
        dbname="projeto_infoeducacao",
        user="user_infoed",
        password="12345",
        host="localhost",
        port=5432
    )

@app.post("/login")
def login(dados: LoginRequest):
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Buscar cduser para o email e senha
        cur.execute(
            "SELECT cduser FROM usuarios WHERE email = %s AND senha = %s",
            (dados.email, dados.senha)
        )
        user = cur.fetchone()
        if user is None:
            raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return {"msg": "Login efetuado com sucesso!", "cduser": user[0]}
