#! /bin/bash

# This script runs within the [Python Image](https://hub.docker.com/_/python/) and updates the
# tests to the latest on master, then runs the tests.

set -e

cd /usr/src/app
git pull https://github.com/mozilla/build-scope-tests master
nosetests
