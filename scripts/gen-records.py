#!/usr/bin/python3

from pathlib import Path

from lib.adoc_generator import AsciiDocGenerator
from lib.constants import INCLUDE_PATH
from lib.process_yamls import process_yamls

stf_record_include = INCLUDE_PATH / 'stf-record.adoc'

yaml_data = process_yamls('records', ['name', 'enum', 'desc'])

with AsciiDocGenerator('stf-records.adoc') as record_list_file:
    for yaml_file, data in yaml_data:
        adoc_filename = Path(yaml_file).with_suffix('.adoc')
        with AsciiDocGenerator(adoc_filename, src_file=yaml_file) as output_file:
            output_file.define_var('record-name', data['name'])
            output_file.define_enum('record-enum', data['enum'])
            if 'mandatory' in data:
                output_file.define_var('record-mandatory', data['mandatory'])
            output_file.include(stf_record_include, tag='record-fields')
            output_file.write_fields(data)
            output_file.include(stf_record_include, tag='record-desc')
            output_file.write_line(data['desc'])
            output_file.include(stf_record_include, tag='record-end')

        record_list_file.include(adoc_filename)
        record_list_file.write_line()
