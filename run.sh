#!/bin/bash

docker run --name uncover_jpeg_stego_attrib --tty --rm --volume=$(realpath ./io):/home/attrib/io uncover_jpeg_stego_attrib:latest "$@"

exit 0
