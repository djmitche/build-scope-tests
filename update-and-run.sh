#! /bin/bash

# This script runs within the [Python Image](https://hub.docker.com/_/python/) and updates the
# tests to the latest on master, then runs the tests.

set -e

cd /usr/src/app
git fetch https://github.com/mozilla/build-scope-tests master
git reset --hard FETCH_HEAD
nosetests
