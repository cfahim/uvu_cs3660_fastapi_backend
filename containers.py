# containers.py
from dependency_injector import containers, providers

from db.db import DatabaseFactory
from repositories.rbac_repository import RbacRepository
from repositories.swapi_repository import SWAPIRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthorizationService
from services.login_service import LoginService
from services.rbac_service import RbacService
from services.swapi_service import SWAPIService

import logging

from services.user_service import UserService

# Create a shared logger instance (could be more complex, e.g., module-based)
logger = logging.getLogger("cs3660backend")
logger.setLevel(logging.DEBUG)

# Define a formatter
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create a handler and attach the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "controllers.login_controller", 
            "controllers.swapi_controller",
            "controllers.rbac_controller",
            "controllers.user_controller",
        ]
    )

    db_factory = providers.Singleton(DatabaseFactory)

    logger = providers.Object(logger)

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
        user_repository=user_repository,
        logger=logger
    )

    rbac_repository = providers.Factory(
        RbacRepository,
        db=db_factory
    )
    rbac_service = providers.Factory(
        RbacService,
        rbac_repository=rbac_repository
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        rbac_repository=rbac_repository,
        logger=logger
    )