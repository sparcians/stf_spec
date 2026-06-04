#!/usr/bin/env python3

from pathlib import Path

from lib.adoc_generator import AsciiDocGenerator
from lib.constants import INCLUDE_PATH
from lib.process_yamls import process_yamls

yaml_data = process_yamls('records', ['name', 'enum'])

multi_pairs = {
    'InstMemContentRecord': 'InstMemAccessRecord',
    'BusMasterContentRecord': 'BusMasterAccessRecord',
    'EventPCTargetRecord': 'EventRecord'
}

irg_end_records = {
    'Inst16Record': 'Inst32Record'
}

exceptions = [
    '<<InstPCTargetRecord>> may appear after <<PageTableWalkRecord>> or <<InstRegRecord>>',
    '<<InstRegRecord>> may appear after <<PageTableWalkRecord>>, <<InstMemContentRecord>>, or <<BusMasterContentRecord>>'
]

def is_allowed(record_data):
    return record_data.get('allowed', True)

def is_header_only(record_data):
    return record_data.get('header_only', False)

def order_required(record_data):
    return record_data.get('order_requirement', True)

def is_transaction(record_data):
    return record_data.get('transaction_record', False)

def is_instruction(record_data):
    return record_data.get('instruction_record', False)

disallowed_records = [(k, v) for k,v in yaml_data if not is_allowed(v)]
header_records = [(k, v) for k,v in yaml_data if is_header_only(v)]
any_order_records = [(k, v) for k,v in yaml_data if not order_required(v)]
inst_ordered_records = [(k, v) for k,v in yaml_data if not is_header_only(v) and order_required(v) and is_allowed(v) and is_instruction(v)]
transaction_records = [(k, v) for k,v in yaml_data if not is_header_only(v) and order_required(v) and is_allowed(v) and is_transaction(v)]

def superscript_tag(tag):
    return f'^_{tag}_^'

transaction_tag = superscript_tag('T')
instruction_tag = superscript_tag('I')
required_unique_tag = superscript_tag('1')
at_least_one_tag = superscript_tag('+')
required_if_prev_tag = superscript_tag('‡')
zero_or_one_tag = superscript_tag('?')

record_tags = {
    'Inst32Record': required_unique_tag,
    'Inst16Record': required_unique_tag,
    'InstPCTargetRecord': zero_or_one_tag,
    'InstMemContentRecord': required_if_prev_tag,
    'InstIEMRecord': zero_or_one_tag,
    'PageTableWalkRecord': zero_or_one_tag,
    'BusMasterContentRecord': required_if_prev_tag,
    'STFIdentifierRecord': required_unique_tag,
    'VersionRecord': required_unique_tag,
    'ISARecord': required_unique_tag,
    'TraceInfoRecord': at_least_one_tag,
    'TraceInfoFeatureRecord': at_least_one_tag,
    'VLenConfigRecord': zero_or_one_tag,
    'ProtocolIDRecord': required_unique_tag,
    'ISAExtendedRecord': zero_or_one_tag,
    'EndHeaderRecord': required_unique_tag
}

trace_type_tag_note = f'''{instruction_tag} indicates a record **may only appear in an instruction trace**. +
{transaction_tag} indicates a record **may only appear in a transaction trace**.'''

with AsciiDocGenerator('stf-record-order.adoc') as record_order_file:
    def write_record(name, ordered = False, note = None):
        if isinstance(note, list):
            note = ''.join(note).replace('^^', '').replace('__', '')

        record_order_file.write_line(f'{"." if ordered else "*"} <<{name}>>{note if note else ""}')

    def write_with_tag(data):
        name = data['name']
        tags = record_tags.get(name)
        tags = [tags] if tags else []
        if is_transaction(data):
            tags += transaction_tag
        elif is_instruction(data):
            tags += instruction_tag
        write_record(name, False, tags if tags else None)

    record_order_file.write_header('Invalid Records', 4)
    record_order_file.write_line('The following records **may not appear** in a trace:')
    record_order_file.write_line()

    for yaml_file, data in disallowed_records:
        write_record(data['name'])

    record_order_file.write_thematic_break()
    record_order_file.write_header('Miscellaneous Records', 4)
    record_order_file.write_line('The following records **may appear at any time** in a trace:')
    record_order_file.write_line()
    record_order_file.write_note_block(trace_type_tag_note)
    record_order_file.write_line()

    for yaml_file, data in any_order_records:
        write_with_tag(data)

    record_order_file.write_thematic_break()
    record_order_file.write_header('Header Records', 4)
    record_order_file.write_line('The following records **may only appear in the trace header**:')
    record_order_file.write_line()
    record_order_file.write_note_block(f'''{required_unique_tag} indicates a record **must appear exactly once** in the header. +
    {zero_or_one_tag} indicates that a record **may appear at most once** in the header. +
    {at_least_one_tag} indicates a record **must appear at least once** in the header. +
    {trace_type_tag_note}''')
    record_order_file.write_line()

    for yaml_file, data in header_records:
        write_with_tag(data)

    record_order_file.write_thematic_break()
    record_order_file.write_header('Instruction Records', 4)
    record_order_file.write_line('These records **may only appear in an instruction trace** and **must be written in the following order** within an IRG (see <<Exceptions>>):')
    record_order_file.write_note_block(f'''{required_unique_tag} indicates a record **must appear exactly once** in an IRG. +
    {zero_or_one_tag} indicates that a record **may appear at most once** in an IRG. +
    {required_if_prev_tag} indicates that a record is **required when the preceding record type is present** in an IRG. +
    All other records are optional and may appear multiple times in an IRG.''')
    record_order_file.write_line()

    for yaml_file, data in inst_ordered_records:
        name = data['name']
        write_record(name, True, record_tags.get(name))
        if name in multi_pairs:
            record_order_file.write_line('+')
            record_order_file.write_note_block(f'This combination (<<{multi_pairs[name]}>>, <<{name}>>) may be repeated multiple times in a row as needed.')
        if name in irg_end_records:
            record_order_file.write_line('+')
            record_order_file.write_important_block(f'<<{irg_end_records[name]}>> and <<{name}>> signal the end of an IRG. Only one of these records may be present in an IRG.')

    record_order_file.write_line()
    record_order_file.write_header('Exceptions', 5)
    record_order_file.write_line('The following exceptions apply to the above IRG ordering rules:')
    record_order_file.write_line()

    for excp in exceptions:
        record_order_file.write_line(f'* {excp}')

    record_order_file.write_thematic_break()
    record_order_file.write_header('Transaction Records', 4)
    record_order_file.write_line('These records **may only appear in a transaction trace**:')
    record_order_file.write_line()

    for yaml_file, data in transaction_records:
        write_record(data['name'])
