#!/bin/bash

version=$(git describe --tags `git rev-list --tags --max-count=1`)
if [[ "$version" != "" ]]
then
	echo ${version#v}
else
	echo "0.1.0"
fi
