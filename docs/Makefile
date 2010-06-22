# Open Cloud Computing Interface (OCCI)
# Author: Sam Johnston <samj@samj.net> 2009-04-10
# Creates documents in various formats from DocBook v5 source

XSL=~/Library/XML/XSL/docbook-xsl-ns-1.75.2

ALL_XML_SRC		:= $(wildcard *.xml)
ALL_HTML_OUT	:= $(subst xml,html,$(ALL_XML_SRC))
ALL_PDF_OUT		:= $(subst xml,pdf,$(ALL_XML_SRC))

all: html pdf

html: $(ALL_HTML_OUT)

pdf: $(ALL_PDF_OUT)

%.html: %.xml
	xsltproc --output $@ --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/xhtml-1_1/docbook.xsl $<

%.fo: %.xml
	xsltproc --output $@ --xinclude --stringparam paper.type A4 --stringparam generate.toc "" $(XSL)/fo/docbook.xsl $<

%.pdf: %.fo
	java org.apache.fop.cli.Main -fo $< -pdf $@
