from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Usuario(BaseModel):
    nome: str
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

@app.post("/usuarios")
def cadastrar_usuario(usuario: Usuario):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (usuario.nome, usuario.email, usuario.senha)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"msg": "Usuário cadastrado com sucesso!"}
