#!/bin/bash
PYTHONPATH=polyhedral/vendor
rm -rv "$PYTHONPATH"/*
pip3 install -t "$PYTHONPATH" -r vendor.txt
