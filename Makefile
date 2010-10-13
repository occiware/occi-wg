
SOURCE := $(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)

all:
	dia -t png dia/*.dia
	pdflatex ${SOURCE}
	# bibtex
	pdflatex ${SOURCE}

show: all
	evince *.pdf

show-mac: all
	open *.pdf

clean:
	rm -rf *.toc *.log *.pdf *.aux *.png
