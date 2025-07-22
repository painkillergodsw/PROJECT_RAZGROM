from fastapi import APIRouter, Depends, Body

from HTTPExceptions import project_not_exists
from schemas import ProjectSchema, MainDomainSchema
from models import Project, MainDomain
from db.dep.depends import get_session
from schemas import UserSchema, CreateProject
from depends import get_user

router = APIRouter(prefix="/core")


@router.post("/create-project")
async def create_project(
    project_schema: CreateProject = Body(),
    user: UserSchema = Depends(get_user),
    session=Depends(get_session),
):
    project_mgnr = Project.manager(session)
    main_domain_mngr = MainDomain.manager(session)
    project = await project_mgnr.add({"name": project_schema.name, "user_id": user.id})
    await main_domain_mngr.bulk_add(
        [
            {"domain": m_domain, "project_id": project.id}
            for m_domain in project_schema.main_domains
        ]
    )
    main_domains = await main_domain_mngr.get_list({"project_id": project.id})
    return ProjectSchema(
        name=project.name,
        id=project.id,
        main_domains=[
            MainDomainSchema(id=main_domain.id, domain=main_domain.domain)
            for main_domain in main_domains
        ],
    )


@router.get("/get-project/{project_id}")
async def get_project(
    project_id: int,
    user: UserSchema = Depends(get_user),
    session=Depends(get_session),
):
    project_mgnr = Project.manager(session)
    project = await project_mgnr.get_one_or_none({"user_id": user.id, "id": project_id})
    if project:
        return ProjectSchema(
            name=project.name,
            id=project.id,
            main_domains=[
                MainDomainSchema(id=main_domain.id, domain=main_domain.domain)
                for main_domain in project.main_domains
            ],
        )
    raise project_not_exists


@router.get("/get-projects")
async def get_projects(
    user: UserSchema = Depends(get_user),
    session=Depends(get_session),
):
    prjct_mngr = Project.manager(session)
    projects = await prjct_mngr.get_list({"user_id": user.id})

    projects_response = []
    for project in projects:
        projects_response.append(
            ProjectSchema(
                name=project.name,
                id=project.id,
                main_domains=[
                    MainDomainSchema(id=main_domain.id, domain=main_domain.domain)
                    for main_domain in project.main_domains
                ],
            )
        )

    return {"projects": projects_response}


@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
