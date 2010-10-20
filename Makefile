
SOURCE:=$(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)
PDFS=$(SOURCE:.tex=.pdf)

dias:
	dia -t png dia/*.dia

%.pdf:
	while (pdflatex $* ; \
	grep -q "Rerun to get cross" $*.log ) do true ; \
	done

all: dias
	for item in $(PDFS) ; do \
	make $$item ; \
	done

show: all
	evince *.pdf

show-mac: all
	open *.pdf

clean:
	rm -rf *.toc *.log *.pdf *.aux *.png *.dvi
