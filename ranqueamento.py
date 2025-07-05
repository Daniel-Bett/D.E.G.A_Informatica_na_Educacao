from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from datetime import datetime
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados
class RanqueamentoRequest(BaseModel):
    cduser: int
    pontos: int
    materia: str
    serie: str

class RanqueamentoResponse(BaseModel):
    id: int
    cduser: int
    nome: str
    pontos: int
    materia: str
    serie: str

def get_conn():
    return psycopg2.connect(
        dbname="projeto_infoeducacao",
        user="user_infoed",
        password="12345",
        host="localhost",
        port=5432
    )

@app.post("/ranqueamento")
def inserir_ranqueamento(dados: RanqueamentoRequest):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO ranqueamento (cduser, pontos, materia, serie)
            VALUES (%s, %s, %s, %s)
        """, (dados.cduser, dados.pontos, dados.materia, dados.serie))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"msg": "Ranqueamento inserido com sucesso"}

@app.get("/ranqueamento/{materia}", response_model=List[RanqueamentoResponse])
def listar_ranqueamento(materia: str):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id,r.cduser, u.nome, pontos, materia, serie
            FROM ranqueamento r
			inner join usuarios u
			on u.cduser = r.cduser
            WHERE materia = %s
            ORDER BY pontos DESC
        """, (materia,))
        resultados = cur.fetchall()
        return [
            RanqueamentoResponse(
                id=r[0],
                cduser=r[1],
                nome=r[2],
                pontos=r[3],
                materia=r[4],
                serie=r[5]
            ) for r in resultados
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
