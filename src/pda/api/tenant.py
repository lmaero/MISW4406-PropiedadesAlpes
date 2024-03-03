import json

from flask import Response
from flask import request

from pda.modules.tenant.application.commands.create_tenant import CreateTenant
from pda.modules.tenant.application.mappers import TenantMapperDTOJson
from pda.modules.tenant.application.queries.get_tenant import GetTenant
from pda.modules.tenant.application.services import TenantService
from pda.seedwork.application.commands import execute_command
from pda.seedwork.application.queries import execute_query
from pda.seedwork.domain.exceptions import DomainException
from pda.seedwork.presentation import api

bp = api.create_blueprint("tenant", "/tenant")


@bp.route("/", methods=("POST",))
def create_tenant():
    try:
        tenant_data = request.json

        tenant_mapper = TenantMapperDTOJson()
        tenant_dto = tenant_mapper.external_to_dto(tenant_data)

        sr = TenantService()
        final_dto = sr.create_tenant(tenant_dto)

        return tenant_mapper.dto_to_external(final_dto)
    except DomainException as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@bp.route("/command", methods=("POST",))
def create_tenant_command():
    try:
        tenant_data = request.json

        tenant_mapper = TenantMapperDTOJson()
        tenant_dto = tenant_mapper.external_to_dto(tenant_data)

        command = CreateTenant(
            tenant_dto.created_at,
            tenant_dto.updated_at,
            tenant_dto.id,
            tenant_dto.name,
            tenant_dto.email,
            tenant_dto.guarantor_name,
        )

        execute_command(command)

        return Response("{}", status=202, mimetype="application/json")
    except DomainException as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@bp.route("/", methods=("GET",))
@bp.route("/<identifier>", methods=("GET",))
def get_tenant_by_id(identifier=None):
    if identifier:
        sr = TenantService()
        tenant_mapper = TenantMapperDTOJson()

        return tenant_mapper.dto_to_external(sr.get_tenant_by_id(identifier))
    else:
        return [{"message": "GET!"}]


@bp.route("/query", methods=("GET",))
@bp.route("/query/<identifier>", methods=("GET",))
def get_tenant_query_by_id(identifier=None):
    if identifier:
        tenant = execute_query(GetTenant(identifier))
        tenant_mapper = TenantMapperDTOJson()

        return tenant_mapper.dto_to_external(tenant)
    else:
        return [{"message": "GET!"}]
