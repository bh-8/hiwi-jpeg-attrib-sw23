#!/bin/bash

docker run --name stegoattrib --tty --rm --volume=$(realpath ./samples):/home/attrib/samples stegoattrib:latest "$@"

exit 0
