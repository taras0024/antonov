import datetime
from dataclasses import dataclass
from typing import NewType

RelationType = NewType('Relation', int)


@dataclass
class Factory:
    name: str
    _id: int = None


@dataclass
class Building:
    name: str
    factory_id: RelationType
    _id: int = None


@dataclass()
class RepairOrganization:
    name: str
    _id: int = None


@dataclass
class Contract:
    number: int
    price: float
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    factory_id: RelationType
    building_id: RelationType
    repair_organization_id: RelationType
    _id: int = None
