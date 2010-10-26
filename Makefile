
TEX=pdflatex
DIA=dia
VIEW=evince

SOURCE:=$(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)
PDFS=$(SOURCE:.tex=.pdf)

all: dias
	for item in $(PDFS) ; do \
	make $$item ; \
	done

dias:
	$(DIA) -t png dia/*.dia

%.pdf: %.tex
	while ($(TEX) $* ; \
	grep -q "Rerun to get cross" $*.log ) do true ; \
	done

show: all
	$(VIEW) *.pdf

show-mac: all
	open *.pdf

clean:
	rm -rf *.toc *.log *.pdf *.aux *.png *.dvi
