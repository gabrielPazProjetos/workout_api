from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate

from app.database import get_db
from app.models.atleta import Atleta
from app.schemas.atleta import AtletaCreate, AtletaOut
from app.exceptions import atleta_cpf_duplicado

router = APIRouter()

@router.post("/", response_model=AtletaOut)
def criar_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    novo = Atleta(**atleta.dict())
    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except IntegrityError:
        db.rollback()
        atleta_cpf_duplicado(atleta.cpf)

@router.get("/", response_model=Page[AtletaOut])
def listar_atletas(
    nome: str = Query(None),
    cpf: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Atleta)
    if nome:
        query = query.filter(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Atleta.cpf == cpf)
    return paginate(query.all())
