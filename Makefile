# Open Cloud Computing Interface (OCCI)
# Author: Sam Johnston <samj@samj.net> 2009-04-10
# Creates documents in various formats from DocBook v5 source

XSL=~/Library/XML/XSL/docbook-xsl-ns-1.75.2

all: html pdf

html: occi-book.html occi-core.html

pdf: occi-book.pdf occi-core.pdf

occi-book.html: occi-book.xml
	xsltproc --output occi-book.html --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/xhtml-1_1/docbook.xsl occi-book.xml

occi-book.fo: occi-book.xml
	xsltproc --output occi-book.fo --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/fo/docbook.xsl occi-book.xml

occi-book.pdf: occi-book.fo
	java org.apache.fop.cli.Main -fo occi-book.fo -pdf occi-book.pdf

occi-core.html: occi-core.xml
	xsltproc --output occi-core.html --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/xhtml-1_1/docbook.xsl occi-core.xml

occi-core.fo: occi-core.xml
	xsltproc --output occi-core.fo --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/fo/docbook.xsl occi-core.xml

occi-core.pdf: occi-core.fo
	java org.apache.fop.cli.Main -fo occi-core.fo -pdf occi-core.pdf
