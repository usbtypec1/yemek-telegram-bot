from dishka import Provider

from bootstrap.ioc.di_providers.food_menu_infrastructure import (
    FoodMenuInfrastructureProvider,
)
from bootstrap.ioc.di_providers.sqla_persistence_infrastructure import (
    SQLAlchemyPersistenceInfrastructureProvider,
)


def get_providers() -> tuple[Provider, ...]:
    return (
        SQLAlchemyPersistenceInfrastructureProvider(),
        FoodMenuInfrastructureProvider(),
    )
