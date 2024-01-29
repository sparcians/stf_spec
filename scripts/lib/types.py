from typing import Union
from typing_extensions import TypedDict

class EnumDict(TypedDict):
    name: str
    val: int

class BaseFieldDict(TypedDict):
    start: Union[int, str]
    desc: str

class FieldDict(BaseFieldDict, total=False):
    end: Union[int, str]

class BaseYamlDict(TypedDict):
    name: str
    enum: EnumDict

class BaseRecordDict(BaseYamlDict):
    desc: str

class RecordDict(BaseRecordDict, total=False):
    mandatory: str
    fields: list[FieldDict]

class ChannelDict(BaseYamlDict, total=False):
    fields: list[FieldDict]

class ProtocolDict(RecordDict, total=False):
    channels: list[ChannelDict]
