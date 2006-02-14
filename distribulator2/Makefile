######################################################################
#
# $Id$
#
######################################################################

all:
	echo "Not implemented."

clean:
	rm -rf build
	rm -rf epydoc
	rm -rf lib
	rm conf/config.xml
	find . -name '*.pyc' | xargs rm > /dev/null 2>&1

count:
	find . -name '*.py' | xargs cat | wc -l

docgen:
	rm -rf epydoc/*
	cd epydoc
	epydoc --html --name "The Distribulator API Documentation" --url "http://distribulator.sourceforge.net/" --output epydoc distribulator/engine/ distribulator/generic/

symlink:
	cd conf/; ln -s config.xml.dist config.xml
	mkdir lib
	mkdir lib/python2.3
	mkdir lib/python2.3/site-packages
	mkdir lib/python2.4
	mkdir lib/python2.4/site-packages
	cd lib/python2.3/site-packages/; ln -s ../../../distribulator
	cd lib/python2.4/site-packages/; ln -s ../../../distribulator
