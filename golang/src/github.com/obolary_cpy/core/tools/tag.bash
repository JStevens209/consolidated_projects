#!/bin/bash

if (( $# != 2 ))
then 
	echo "usage: tag [current-semver] [new-semver]"
	echo "for example, 'tag v1.2.1 v1.2.3'"
else
	current=$(pwd)
	echo ""
	echo "******* TAG VERSION ${current} AS ${1} *******"

	version=$(git describe --abbrev=0 --tags)
	echo "******* CURRENT VERSION ${version}"

	if [[ $version != ${1} ]]
	then
		echo "******* VERSION NOT EXPECTED, ${1}"
	else
		git tag ${2}
		git push origin develop --tags
		echo "******* NEW VERSION $(git describe --abbrev=0 --tags)"
	fi
fi

