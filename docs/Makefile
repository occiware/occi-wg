# Open Cloud Computing Interface (OCCI)
# Author: Sam Johnston <samj@samj.net> 2009-04-10
# Creates documents in various formats from DocBook v5 source

XSL=~/Library/XML/XSL/docbook-xsl-ns-1.75.2

all: xhtml

xhtml: occi-book.xml
	xsltproc --output occi-book.html --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/xhtml-1_1/docbook.xsl occi-book.xml

pdf: occi-book.xml
	xsltproc --output occi-book.fo --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/fo/docbook.xsl occi-book.xml
	java org.apache.fop.cli.Main -fo occi-book.fo -pdf occi-book.pdf

core: occi-core.xml
	xsltproc --output occi-core.html --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/xhtml-1_1/docbook.xsl occi-core.xml
	xsltproc --output occi-core.fo --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/fo/docbook.xsl occi-core.xml
	java org.apache.fop.cli.Main -fo occi-core.fo -pdf occi-core.pdf

http: occi-http.xml
	xsltproc --output occi-http.html --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/xhtml-1_1/docbook.xsl occi-http.xml
	xsltproc --output occi-http.fo --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/fo/docbook.xsl occi-http.xml
	java org.apache.fop.cli.Main -fo occi-http.fo -pdf occi-http.pdf

infrastructure: occi-infrastructure.xml
	xsltproc --output occi-infrastructure.html --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/xhtml-1_1/docbook.xsl occi-infrastructure.xml
	xsltproc --output occi-infrastructure.fo --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/fo/docbook.xsl occi-infrastructure.xml
	java org.apache.fop.cli.Main -fo occi-infrastructure.fo -pdf occi-infrastructure.pdf

