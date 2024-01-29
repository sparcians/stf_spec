from pathlib import Path
from typing import Optional, Union
from yaml import load
try:
    from yaml import CLoader as Loader  # type: ignore
except ImportError:
    from yaml import Loader  # type: ignore

from lib.types import EnumDict, RecordDict, ChannelDict, ProtocolDict

def check_required_field(
    yaml_file: Union[str, Path],
    yaml_data: Union[RecordDict, ChannelDict, ProtocolDict],
    field: str
) -> None:
    def check_required_enum_field(enum_field: Union[str, Path]) -> None:
        if enum_field not in yaml_data['enum']:
            raise RuntimeError(f"Required 'enum' subfield '{enum_field}' missing from {yaml_file}")

    if yaml_data is None:
        raise RuntimeError(f'YAML {yaml_file} is empty')

    if field not in yaml_data:
        raise RuntimeError(f"Required field '{field}' missing from {yaml_file}")

    if field == 'enum':
        check_required_enum_field('name')
        check_required_enum_field('val')

def process_yamls(
    path: Union[str, Path],
    required_fields: Optional[list[str]] = None
) -> list[tuple[Path, Union[RecordDict, ProtocolDict]]]:
    yaml_data: dict[Path, Union[RecordDict, ProtocolDict]] = {}

    if required_fields is None:
        required_fields = []

    for yaml_file in Path(path).glob('*.yml'):
        with open(yaml_file, 'r') as input_file:
            data = load(input_file, Loader=Loader)
            for field in required_fields:
                check_required_field(yaml_file, data, field)
            yaml_data[yaml_file] = data

    return sorted(yaml_data.items(), key = lambda x: x[1]['enum']['val'])
