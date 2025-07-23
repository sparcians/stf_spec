#!/bin/bash

./scripts/bundle-setup.sh

bundle exec asciidoctor-pdf -d book -a revnumber=$(git describe --abbrev=0) -o generated/stf-spec.pdf stf-spec.adoc
