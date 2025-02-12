from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.schemas import Adherent, AdherentCreate, LoginRequest,Token
from app.use_cases import adherent_use_case

router = APIRouter()

@router.get("/{adherent_id}", response_model=Adherent)
async def get_adherent(adherent_id: str):
    adh = await adherent_use_case.get_adherent_use_case(adherent_id)
    if adh:
        return adh
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found")

@router.get("/", response_model=List[Adherent])
async def get_adherents(role: Optional[str] = None, skip: int = 0, limit: int = 10):
    adherents = await adherent_use_case.list_adherents_use_case(role, skip, limit)
    if adherents:
        return adherents
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No adherents found")

@router.post("/", response_model=Adherent, status_code=status.HTTP_201_CREATED)
async def create_adherent(adherent: AdherentCreate):
    created_adh = await adherent_use_case.create_adherent_use_case(adherent)
    return created_adh

@router.get("/{adherent_id}", response_model=Adherent)
async def get_adherent(adherent_id: str):
    adh = await adherent_use_case.get_adherent_use_case(adherent_id)
    if adh:
        return adh
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found")

@router.get("/", response_model=List[Adherent])
async def get_adherents(role: Optional[str] = None, skip: int = 0, limit: int = 10):
    adherents = await adherent_use_case.list_adherents_use_case(role, skip, limit)
    if adherents:
        return adherents
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No adherents found")

@router.post("/", response_model=Adherent, status_code=status.HTTP_201_CREATED)
async def create_adherent(adherent: AdherentCreate):
    created_adh = await adherent_use_case.create_adherent_use_case(adherent)
    return created_adh

@router.put("/{adherent_id}", response_model=Adherent)
async def update_adherent(adherent_id: str, adherent: AdherentCreate):
    updated_adh = await adherent_use_case.update_adherent_use_case(adherent_id, adherent)
    if updated_adh:
        return updated_adh
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found")

@router.delete("/{adherent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adherent(adherent_id: str):
    success = await adherent_use_case.delete_adherent_use_case(adherent_id)
    if success:
        return  # HTTP 204 No Content
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found")

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    token_data = await adherent_use_case.login_use_case(login_request.login, login_request.password)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect login or password")
    return token_data