#!/bin/bash
# $1 Replacement name for Trakka
# Will setup the build environment for publishing to alternative CLI repos.

NORMAL=$1
LOWER=$(echo $NORMAL | awk '{print tolower($0)}')

sed -i.bak "s/\"trakka\"/\"$LOWER\"/g" setup.py
sed -i.bak "s/an Trakka instance/a $NORMAL instance/g" setup.py
sed -i.bak "s/trakka=trakka.main:main/$LOWER=trakka.main:main/g" setup.py
rm setup.py.bak

sed -i.bak "s/\"trakka\"/\"$LOWER\"/g" pyproject.toml
rm pyproject.toml.bak

sed -i.bak "s/\"trakka\"/\"$LOWER\"/g" trakka/__init__.py
rm trakka/__init__.py.bak

sed -i.bak "s/Trakka/$NORMAL/g" README.md
sed -i.bak "s/trakka/$LOWER/g" README.md
sed -i.bak "s/$LOWER-admin/trakka-admin/g" README.md
