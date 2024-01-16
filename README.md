# stf_spec
An open-source Simple Tracing Format specification

Simple Trace Format (STF) is a binary file format for storing instruction traces, agnostic of instruction
set architecture. The format defines a standard for capturing information related to instructions,
associated register values, memory access addresses and data associated with them, as well as
additional context information such as page table walk, interrupts, bus/fabric transaction
addresses/data, etc. This document also specifies how tools generating and/or modifying traces can
express information which can aid the tools consuming the traces to interpret them appropriately.

An online version of this spec is available [here](generated/stf-spec-github.adoc).
