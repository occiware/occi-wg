
SOURCE := $(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)

all:
	dia -t png dia/*.dia
	for number in ${SOURCE} ; do \
	pdflatex $$number ; \
	pdflatex $$number ; \
	done

show: all
	evince *.pdf

show-mac: all
	open *.pdf

clean:
	rm -rf *.toc *.log *.pdf *.aux *.png *.dvi
