from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


class BinaryRelationModel(BaseModel):
    set_of_elements: Optional[str] = Field(
        default=None,
        description="Множество, на котором задано бинарное отношение.\n"
        "Может быть сгенерировано автоматически на основе бинарного отношения",
        examples=["1,2,3"],
    )
    binary_relation: str = Field(
        default="",
        description="Бинарное отношение, заданное парами",
        examples=["(1,2),(2,2),(2,3),(3,2)"],
    )

    def get_set_of_elements(self) -> Optional[set[str]]:
        if self.set_of_elements:
            return set(self.set_of_elements.split(","))

    def get_binary_relation(self) -> set[tuple[str, str]]:
        # maybe we need regex here
        binary_relation = self.binary_relation.replace(" ", "")
        binary_relation = binary_relation.strip("()")
        binary_relation_list = binary_relation.split("),(")
        relation_set = set()
        for pair in binary_relation_list:
            elements = pair.split(",")
            el1, el2 = elements[0], elements[1]
            relation_set.add((el1, el2))
        return relation_set


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
