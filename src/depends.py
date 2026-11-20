from typing import Annotated

from fastapi.params import Query

from schemas.pagination import PaginationParams

PaginationDep = Annotated[PaginationParams, Query()]
