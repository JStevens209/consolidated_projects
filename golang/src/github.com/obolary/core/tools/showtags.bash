#!/bin/bash
for i in $(find . -name ".git")
do 
	cd $i/..
	echo $(pwd)
	echo "++ semver ++"
	echo $(git describe --abbrev=0 --tags)
	echo "+++ refs +++"
	git show-ref
	echo "************"
	cd -
done
