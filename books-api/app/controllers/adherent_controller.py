from typing import List, Optional

from app.schemas import Adherent, AdherentCreate, Loan, LoginRequest, Token
from app.use_cases import adherent_use_case
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get(
    "/{adherent_id}",
    response_model=Adherent,
    summary="Retrieve an adherent",
)
async def get_adherent(adherent_id: str):
    """
    Retrieve an adherent by its unique identifier.

    **Path Parameter:**
    - **adherent_id**: The unique identifier of the adherent.

    **Example:**
    ```
    GET /adherents/60b725f10c9f1e23d8f3a3e9
    ```
    """
    adh = await adherent_use_case.get_adherent_use_case(adherent_id)
    if adh:
        return adh
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found"
    )


@router.get(
    "/",
    response_model=List[Adherent],
    summary="List adherents",
)
async def get_adherents(role: Optional[str] = None, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of adherents.

    **Query Parameters:**
    - **role**: (Optional) Filter adherents by role.
    - **skip**: Number of records to skip.
    - **limit**: Maximum number of records to return.

    **Example:**
    ```
    GET /adherents?role=user&skip=0&limit=10
    ```
    """
    adherents = await adherent_use_case.list_adherents_use_case(role, skip, limit)
    if adherents:
        return adherents
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No adherents found"
    )


@router.post(
    "/",
    response_model=Adherent,
    status_code=status.HTTP_201_CREATED,
    summary="Create an adherent",
)
async def create_adherent(adherent: AdherentCreate):
    """
    Create a new adherent.

    **Request Body:**
    - **first_name**: The first name of the adherent.
    - **last_name**: The last name of the adherent.
    - **membership number": The membership number of the adherent.
    - **login**: The login username of the adherent.
    - **password**: The password (will be hashed before storage).
    - **role**: The role of the adherent (e.g., "user", "admin").

    **Example:**
    ```
    POST /adherents
    {
      "first_name": "John",
      "last_name": "Doe",
      "membership_number": "string",
      "login": "johndoe",
      "password": "your_password",
      "role": "user"
    }
    ```
    """
    created_adh = await adherent_use_case.create_adherent_use_case(adherent)
    return created_adh


@router.put(
    "/{adherent_id}",
    response_model=Adherent,
    summary="Update an adherent",
)
async def update_adherent(adherent_id: str, adherent: AdherentCreate):
    """
    Update an existing adherent.

    **Path Parameter:**
    - **adherent_id**: The unique identifier of the adherent to update.

    **Request Body:**
    - **first_name**: The new first name.
    - **last_name**: The new last name.
    - **membership number": The new membership number.
    - **login**: The new login username.
    - **password**: The new password.
    - **role**: The new role.

    **Example:**
    ```
    PUT /adherents/60b725f10c9f1e23d8f3a3e9
    {
      "first_name": "John",
      "last_name": "Doe",
      "membership_number": "string",
      "login": "johndoe",
      "password": "new_password",
      "role": "admin"
    }
    ```
    """
    updated_adh = await adherent_use_case.update_adherent_use_case(
        adherent_id, adherent
    )
    if updated_adh:
        return updated_adh
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found"
    )


@router.delete(
    "/{adherent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an adherent",
)
async def delete_adherent(adherent_id: str):
    """
    Delete an adherent by their unique identifier.

    **Example:**
    ```
    DELETE /adherents/60b725f10c9f1e23d8f3a3e9
    ```

    **Response:**
    HTTP 204 No Content
    """
    success = await adherent_use_case.delete_adherent_use_case(adherent_id)
    if success:
        return  # HTTP 204 No Content
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found"
    )


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate an adherent",
)
async def login(login_request: LoginRequest):
    """
    Authenticate an adherent with their login credentials.

    **Request Body:**
    - **login**: The adherent's login username.
    - **password**: The adherent's password.

    **Example:**
    ```
    POST /adherents/login
    {
      "login": "johndoe",
      "password": "your_password"
    }
    ```

    **Response:**
    ```
    {
      "access_token": "jwt_token_here",
      "token_type": "bearer"
    }
    ```
    """
    token_data = await adherent_use_case.login_use_case(
        login_request.login, login_request.password
    )
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password",
        )
    return token_data


@router.get(
    "/{adherent_id}/loans",
    response_model=List[Loan],
    summary="Retrieve loans for an adherent",
)
async def get_loans_for_adherent(adherent_id: str):
    """
    Retrieve a list of loans for a specific adherent.

    **Exemple :**
    ```
    GET /adherents/60b725f10c9f1e23d8f3a3e9/loans
    ```
    """
    loans = await adherent_use_case.get_loans_by_adherent_use_case(adherent_id)
    if loans:
        return loans
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No loans found for this adherent"
    )
