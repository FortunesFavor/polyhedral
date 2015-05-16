#!/bin/bash
PACKAGE="dice"
ZDIR="$HOME/.znc"

ZMODDIR="$ZDIR/modules"
IG="$PWD/.gitignore"
PKG="$PWD/$PACKAGE"

if [ -d "$ZDIR" ]
then
    if [ ! -d "$ZMODDIR" ]
    then
        mkdir "$ZMODDIR"
    fi
else
    echo "ZNC config directory not found."
    exit 1
fi

rsync -avl --delete --exclude-from "$IG" "$PKG" "$ZMODDIR"
