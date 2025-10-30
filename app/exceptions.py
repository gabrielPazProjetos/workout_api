from fastapi import HTTPException

def atleta_cpf_duplicado(cpf: str):
    raise HTTPException(
        status_code=303,
        detail=f"Já existe um atleta cadastrado com o cpf: {cpf}"
    )
