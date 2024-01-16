# STF Record Definitions

The YAML files in this directory are used to auto-generate the documentation for
STF record types (listed under the Specification of Records section in
stf-spec.adoc)

## YAML File Structure

```
name: RecordName
enum:
  name: STF_RECORD_NAME
  val: 255
mandatory: 'YES'/'NO'/message explaining when the record is mandatory
fields:
    - start: 0
      end: 31
      desc: Field description
    - start: 32
      end: 63
      desc: Other field description
desc: |-
  Description of record
```

### Field Descriptions

- `name` (**Required**): The name of the C++ class associated with this record
type
- `enum`
  - `name` (**Required**): The name of the enum value associated with this
record type
  - `value` (**Required**): The integer value associated with the enum
- `mandatory` (**Optional**): If present, will populate the Required field in
the documentation with the given string. If omitted, the Required field will
auto-populate with "NO".
- `fields` (**Optional**): List of fields present in the record. If omitted, the
documentation will auto-populate with a message declaring there are no fields in
the record.
  - `start` (**Required**): The lower bit index (starting from 0) of this field
  - `end` (**Optional**): The upper bit index of this field. If omitted, this
  field will be treated as 1-bit wide
  - `desc` (**Required**): The description for this field
- `desc` (**Required**): The description for this record type
