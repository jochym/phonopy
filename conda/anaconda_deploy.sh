#!/bin/bash

export LBL=$1
export TKN=$2
export GIT_BRANCH=$3

echo "Building: $GIT_BRANCH"
conda build conda --no-anaconda-upload
TRG=`conda build conda --output |sed -e 's/--/-*-/'`
echo "Uploading: $TRG"
anaconda --token $TKN upload --label $LBL $TRG

