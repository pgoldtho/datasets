#!/bin/bash
for zip in ../reg_d/resources/data/*.zip
do
      unzip "$zip" -d ../reg_d/resources/data/
done
