#!/bin/bash

###################
## Gen changelog.md
###################

changeln -t ./changeln/changeln.template \
    -c ./changeln/changeln.yaml \
    -p ./ \
    changelog markdown
