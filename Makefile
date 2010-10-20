
TEX=pdflatex
DIA=dia
VIEW=evince

SOURCE:=$(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)
PDFS=$(SOURCE:.tex=.pdf)

dias:
	$(DIA) -t png dia/*.dia

%.pdf:
	while ($(TEX) $* ; \
	grep -q "Rerun to get cross" $*.log ) do true ; \
	done

all: dias
	for item in $(PDFS) ; do \
	make $$item ; \
	done

show: all
	$(VIEW) *.pdf

show-mac: all
	open *.pdf

clean:
	rm -rf *.toc *.log *.pdf *.aux *.png *.dvi
