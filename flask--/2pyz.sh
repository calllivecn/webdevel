#!/bin/bash
# date 2024-02-03 04:11:47
# author calllivecn <calllivecn@outlook.com>

# pip install packages
PACKS="flask uvicorn"

CWD=$(pwd -P)
TMP=$(mktemp -d -p "$CWD")

DEPEND_CACHE="${CWD}/depend-cache"

if [ -d "$DEPEND_CACHE" ];then
	echo "使用depend-cache ~"
	(cd "$DEPEND_CACHE";cp -rv . "$TMP")
else
	mkdir -v "${DEPEND_CACHE}"
	pip3 install --no-compile --target "$DEPEND_CACHE" $PACKS
	(cd "$DEPEND_CACHE";cp -rv . "$TMP")
fi

clean(){
	echo "clean... ${TMP}"
	rm -rf "${TMP}"
	echo "done"
}

trap clean SIGINT SIGTERM EXIT ERR

cp -v app1.py "${TMP}/"
cp -v server-uvicorn.py "${TMP}/__main__.py"

python -m zipapp --python '/usr/bin/env python' --compress --output flask-uvicorn.pyz "${TMP}" 

