
TEX=pdflatex
BIBTEX=bibtex
DIA=dia
VIEW=evince

SOURCE:=$(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)
PDFS=$(SOURCE:.tex=.pdf)

all:
	for item in $(PDFS) ; do \
	make $$item ; \
	done

%.pdf: %.tex *.sty
	$(TEX) $*

	@if(grep "There were undefined references" $*.log > /dev/null);\
	then \
		$(BIBTEX) $*; \
		$(TEX) $*; \
	fi

	@if(grep "Rerun" $*.log > /dev/null);\
	then \
		$(TEX) $*;\
	fi

show:
	$(VIEW) *.pdf

show-mac: all
	open *.pdf

clean:
	@rm -f *.pdf *.aux *.bbl *.blg *.log *.dvi *.png *~ \
		*.idx *.ilg *.ind *.toc *.lot *.lof *.gz *.out \
		include/contributors.aux

