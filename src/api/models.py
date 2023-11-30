from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


class BinaryRelationModel(BaseModel):
    set_of_elements: Optional[set[Union[str, int]]] = Field(
        default=set(),
        description="Множество, на котором задано бинарное отношение.\n"
        "Может быть сгенерировано автоматически на основе бинарного отношения",
    )
    binary_relation: set[tuple[Union[str, int], Union[str, int]]] = Field(
        default=set(), description="Бинарное отношение, заданное парами"
    )


class GetRelationPropertiesModel(BaseModel):
    properties: list[
        Literal[
            "Рефлексивно",
            "Антирефлексивно",
            "Нерефлексивно",
            "Симметрично",
            "Асимметрично",
            "Антисимметрично",
            "Несимметрично",
            "Транзитивно",
            "Антитранзитивно",
            "Нетранзитивно",
        ]
    ] = Field(default=["Нерефлексивно", "Несимметрично", "Нетранзитивно"])
