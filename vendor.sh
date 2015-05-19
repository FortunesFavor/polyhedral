#!/bin/bash
PYTHONPATH=polyhedral/vendor
rm -r "$PYTHONPATH"/*
pip3 install -t "$PYTHONPATH" -r vendor.txt
