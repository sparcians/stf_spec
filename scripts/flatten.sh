#!/bin/bash

INSTALLED_GEMS_PATH=.bundle/gems

if ! command -v ruby &> /dev/null
then
    echo "This script requires ruby to work. Please install it and try again."
fi

if ! command -v bundle &> /dev/null
then
    echo "This script requires bundler to work. Please run:"
    echo "gem install bundler"
    echo "and try again"
fi

if [ ! -d $INSTALLED_GEMS_PATH ]
then
    bundle --path=$INSTALLED_GEMS_PATH
fi

bundle exec asciidoctor-reducer -o generated/stf-spec-github.adoc stf-spec.adoc
