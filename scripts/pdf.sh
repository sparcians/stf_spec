#!/bin/bash

./scripts/bundle-setup.sh

bundle exec asciidoctor-pdf -d book -a revnumber=$(git tag) -o generated/stf-spec.pdf stf-spec.adoc
