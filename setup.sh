#!/usr/bin/env bash

python resolve-dependencies.py

echo "Generating projects"

xcodegen -s ./FeatureModule/project-resolved.yml
xcodegen -s ./ApiModule/project-resolved.yml
xcodegen -s ./App/project-resolved.yml
