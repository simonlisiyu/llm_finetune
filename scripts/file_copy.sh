#!/bin/bash

echo $#
echo $1
echo $2
echo $3

file_name=$1
base_path=$2
file_path=$3

mkdir -p ${base_path}/${file_path}
cp ${base_path}/${file_name} ${base_path}/${file_path}/${file_name}


