# Open Cloud Computing Interface (OCCI)
# Author: Sam Johnston <samj@samj.net> 2009-04-10
# Creates documents in various formats from DocBook v5 source

XSL=~/Library/XML

all: xhtml

xhtml: occi-book.xml
	xsltproc --output occi-book.html --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/docbook-xsl-ns-1.74.3/xhtml-1_1/docbook.xsl occi-book.xml

pdf: occi-book.xml
	xsltproc --output occi-book.fo --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/docbook-xsl-ns-1.74.3/fo/docbook.xsl occi-book.xml
	java org.apache.fop.cli.Main -fo occi-book.fo -pdf occi-book.pdf
