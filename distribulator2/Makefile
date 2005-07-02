#
# $Id$
#
PYTHON=/usr/local/bin/python

all:
	echo "Not implemented."

clean:
	rm -rf build
	rm -rf lib
	find . -name '*.pyc' | xargs rm > /dev/null 2>&1

count:
	find . -name '*.py' | xargs cat | wc -l

install:
	python setup.py install --prefix=.
