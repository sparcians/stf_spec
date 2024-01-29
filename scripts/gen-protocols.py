#!/usr/bin/python3

from pathlib import Path
from typing import cast

from lib.adoc_generator import AsciiDocGenerator
from lib.constants import INCLUDE_PATH
from lib.process_yamls import process_yamls
from lib.types import ProtocolDict

stf_protocol_include = INCLUDE_PATH / 'stf-protocol.adoc'

yaml_data = process_yamls('protocols', ['name', 'enum', 'desc'])

with AsciiDocGenerator('stf-protocols.adoc') as protocol_list_file:
    for yaml_file, data in yaml_data:
        data = cast(ProtocolDict, data)
        adoc_filename = Path(yaml_file).with_suffix('.adoc')
        with AsciiDocGenerator(adoc_filename, src_file=yaml_file) as output_file:
            output_file.define_var('protocol-name', data['name'])
            output_file.define_enum('protocol-enum', data['enum'])
            output_file.include(stf_protocol_include, tag='protocol-fields')
            output_file.write_fields(data)
            output_file.include(stf_protocol_include, tag='protocol-desc')
            output_file.write_line(data['desc'])
            output_file.include(stf_protocol_include, tag='protocol-end')

            if 'channels' in data:
                for channel in data['channels']:
                    output_file.define_var('channel-name', channel['name'])
                    output_file.define_enum('channel-enum', channel['enum'])
                    output_file.include(stf_protocol_include, tag='channel-fields')
                    output_file.write_fields(channel)

                    output_file.include(stf_protocol_include, tag='channel-end')

        protocol_list_file.include(adoc_filename)
        protocol_list_file.write_line()
