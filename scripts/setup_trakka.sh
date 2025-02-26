#!/bin/bash
# $1 Replacement name for AusTrakka
# Will setup the build environment for publishing to alternative CLI repos.

NORMAL=$1
LOWER=$(echo $NORMAL | awk '{print tolower($0)}')

sed -i.bak "s/\"austrakka\"/\"$LOWER\"/g" setup.py
sed -i.bak "s/an AusTrakka instance/a $NORMAL instance/g" setup.py
sed -i.bak "s/austrakka=austrakka.main:main/$LOWER=austrakka.main:main/g" setup.py
rm setup.py.bak

sed -i.bak "s/\"austrakka\"/\"$LOWER\"/g" pyproject.toml
rm pyproject.toml.bak

sed -i.bak "s/\"AusTrakka\"/\"$NORMAL\"/g" austrakka/__init__.py
rm austrakka/__init__.py.bak
