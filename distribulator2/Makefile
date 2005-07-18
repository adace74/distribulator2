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

symlink:
	cd conf/; ln -s config.xml.dist config.xml
	cd lib/python2.4/site-packages/; ln -s ../../../distribulator
