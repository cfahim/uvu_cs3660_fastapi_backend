# containers.py
from dependency_injector import containers, providers

from db.db import DatabaseFactory
from repositories.swapi_repository import SWAPIRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthorizationService
from services.login_service import LoginService
from services.swapi_service import SWAPIService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["controllers.login_controller", "controllers.swapi_controller"])

    db_factory = providers.Singleton(DatabaseFactory)

    user_repository = providers.Factory(
        UserRepository,
        db=db_factory
    )

    login_service = providers.Factory(
        LoginService,
        user_repository=user_repository
    )

    swapi_repository = providers.Factory(SWAPIRepository)

    swapi_service = providers.Factory(
        SWAPIService,
        swapi_repository=swapi_repository
    )

    auth_service = providers.Factory(
        AuthorizationService,
        user_repository=user_repository
    )
