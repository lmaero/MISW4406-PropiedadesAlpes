from fastapi import APIRouter, status, BackgroundTasks
from tenant.module.application.commands.register_tenant import CommandRegisterTenant
from tenant.seedwork.presentation.dto import AsyncResponse
from tenant.seedwork.application.commands import execute_command

from .dto import RegisterTenant


router = APIRouter()

@router.post("/register", status_code=status.HTTP_202_ACCEPTED, response_model=AsyncResponse)
async def register_tenant(register_tenant: RegisterTenant, background_tasks: BackgroundTasks) -> dict[str, str]:
    command = CommandRegisterTenant(
        name=register_tenant.name,
        last_name=register_tenant.last_name,
        email=register_tenant.email,
        password=register_tenant.password,
        is_bussines=register_tenant.is_bussines
    )
    background_tasks.add_task(execute_command, command)
    return AsyncResponse(mensaje="Tenant register in process")