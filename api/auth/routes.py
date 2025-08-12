from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from . import deps, schemas
from .db import fake_users_db, get_user
from .security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_password,
)

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Realiza o login de um usuário e retorna um token de acesso.
    
    - **usuário**: testuser
    - **senha**: testpassword
    """
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=schemas.Token)
async def refresh_access_token(
    current_user: Annotated[schemas.User, Depends(deps.get_current_active_user)]
):
    """
    Atualiza um token de acesso existente.
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}