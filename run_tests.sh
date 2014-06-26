#!/usr/bin/env bash

make test
pytest_success=$?
make unittest
unittest_success=$?

echo "

*** RESULTS ***"

if [ $pytest_success -eq 0 ]; then
  echo 'pytest suite passed'
else
  echo 'pytest suite failed'
fi

if [ $unittest_success -ne 0 ]; then
  echo 'unittest suite passed'
else
  echo 'unittest suite failed'
fi

if [ $pytest_success -eq 0 -a $unittest_success -ne 0 ]; then
  exit 0
else
  exit 1
fi
