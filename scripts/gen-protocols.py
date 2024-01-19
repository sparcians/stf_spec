#!/usr/bin/python3

import os
from pathlib import Path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def check_required_field(yaml_file, yaml_data, field):
    def check_required_enum_field(enum_field):
        if enum_field not in yaml_data['enum']:
            raise RuntimeError(f"Required 'enum' subfield '{enum_field}' missing from {yaml_file}")

    if yaml_data is None:
        raise RuntimeError(f'Protocol YAML {yaml_file} is empty')

    if field not in yaml_data:
        raise RuntimeError(f"Required field '{field}' missing from {yaml_file}")

    if field == 'enum':
        check_required_enum_field('name')
        check_required_enum_field('val')

yaml_data = {}

generated_dir = Path('generated')

stf_protocol_include = '../../include/stf-protocol.adoc'

for yaml_file in Path('protocols').glob('*.yml'):
    with open(yaml_file, 'r') as input_file:
        data = load(input_file, Loader=Loader)
        check_required_field(yaml_file, data, 'name')
        check_required_field(yaml_file, data, 'enum')
        check_required_field(yaml_file, data, 'desc')
        yaml_data[yaml_file] = data

with open(generated_dir / 'stf-protocols.adoc', 'w') as protocol_list_file:
    for yaml_file, data in sorted(yaml_data.items(), key = lambda x: x[1]['enum']['val']):
        adoc_filename = Path(yaml_file).with_suffix('.adoc')
        output_filename = generated_dir / adoc_filename
        with open(output_filename, 'w') as output_file:
            output_file.write(
                '////\n'
                'DO NOT EDIT. This file was autogenerated by gen-protocols.py.\n'
                f'To make changes to this file, edit {yaml_file} and then run make.\n'
                '////\n'
                f':protocol-name: {data["name"]}\n'
                f':protocol-enum: {data["enum"]["name"]} ({data["enum"]["val"]})\n'
                f'include::{stf_protocol_include}[tag=protocol-fields]\n'
            )
            def write_field(field):
                start_idx = field['start']
                bit_range = str(start_idx)
                if 'end' in field:
                    end_idx = field['end']
                    if isinstance(end_idx, int) and end_idx < start_idx:
                        raise RuntimeError(f"Field end index {end_idx} should be >= start index {start_idx} in {yaml_file}")
                    if end_idx != start_idx:
                        bit_range = f'{field["end"]}:' + bit_range
                output_file.write(f'* b[{bit_range}] {field["desc"]}\n')

            if 'fields' in data:
                for field in data['fields']:
                    write_field(field)
            else:
                output_file.write('b[-1] Protocol has no data, just the descriptor.\n')

            output_file.write(
                f'include::{stf_protocol_include}[tag=protocol-desc]\n'
                f'{data["desc"]}\n'
                f'include::{stf_protocol_include}[tag=protocol-end]\n'
            )

            if 'channels' in data:
                for channel in data['channels']:
                    output_file.write(
                        f':channel-name: {channel["name"]}\n'
                        f':channel-enum: {channel["enum"]["name"]} ({channel["enum"]["val"]})\n'
                        f'include::{stf_protocol_include}[tag=channel-fields]\n'
                    )
                    if 'fields' in channel:
                        for field in channel['fields']:
                            write_field(field)

                    output_file.write(
                        f'include::{stf_protocol_include}[tag=channel-end]\n'
                    )

        protocol_list_file.write(f'include::{adoc_filename}[]\n\n')
