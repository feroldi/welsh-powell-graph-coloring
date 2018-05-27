#!/bin/sh

BASEDIR="$(dirname `readlink -f $0`)"

(
cd $BASEDIR
for N in `ls -1 tests/input`
do
  printf 'TESTCASE %s RUNNING\n' $N
  cat tests/input/$N | python ../main.py - | diff - tests/output/$N
  if [ $? -eq 0 ]; then
    printf 'TESTCASE %s SUCCEEDED\n' $N
  else
    printf 'TESTCASE %s FAILED\n' $N
  fi
done
)
