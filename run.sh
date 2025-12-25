#!/bin/bash

for i in {1..10}
do
  python3  -u  main.py TaskDownloadPage 500 $1
done