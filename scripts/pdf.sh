#!/bin/bash

./scripts/bundle-setup.sh

bundle exec asciidoctor-pdf -o generated/stf-spec.pdf stf-spec.adoc
