"""
app/database/models.py

Import every SQLModel table model here.

The purpose of this module is to make sure all
SQLModel tables are registered in SQLModel.metadata
before create_all() is called.
"""

# Later:
from app.features.identity.infrastructure.sqlmodel.models import UserModel

# from app.features.orders.infrastructure.persistence.sqlmodel.models import (
#     OrderModel,
# )

#
# from app.features.products.infrastructure.persistence.sqlmodel.models import (
#     ProductModel,
# )
