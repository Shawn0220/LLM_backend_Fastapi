"""
@description:自定义分页
"""
from typing import TypeVar, Generic, Sequence

from fastapi import Query
from fastapi_pagination.bases import AbstractParams, RawParams, BasePage
from pydantic import BaseModel, conint

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="页码")  # 设置默认值为1，不能够小于1
    size: int = Query(10, gt=0, le=10000, description="每页数量")  # 设置默认值为10，最大为10000

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            # 更爱page参数起始值从1开始
            offset=self.size * (self.page - 1),
        )


class Page(BasePage[T], Generic[T]):
    page: conint(ge=1)  # type: ignore
    size: conint(ge=1)  # type: ignore

    __params_type__ = Params

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            total: int,
            params: AbstractParams,
    ):
        if not isinstance(params, Params):
            raise ValueError("Page应该与Params一起使用")

        return cls(
            total=total,
            items=items,
            page=params.page,
            size=params.size,
        )
