NAME=OCCI_monitoring

GRAPHS:=                # add graphs to generate, e.g. using fig or dia.
IMAGE:=$(wildcard *.png *.jpg)

# Determine .tex source files by examining the \input{file} in ${NAME}.tex
TEXINCLUDE:=$(patsubst \input{%},%,$(shell grep -o "\\\\input{.*}" ${NAME}.tex))
FILES:=$(foreach file,${TEXINCLUDE},$(addsuffix .tex,${file}))    # add extension to files

REFS=$(wildcard *.bib)

all: pdflatex

${NAME}.pdf: pdflatex

${NAME}.ps: latex

.PHONY: latex pdflatex xelatex

latex: ${NAME}.tex ${GRAPHS} ${FILES} ${REFS}
	latex ${NAME}.tex
	# only run makeindex if there is a \makeindex statement
	egrep "^[^%]*\\\\makeindex" ${NAME}.tex && makeindex ${NAME}.tex ; true
	# only run bibtex if there is a \bibliography statement
	egrep "^[^%]*\\\\bibliography" ${NAME}.tex && bibtex ${NAME}.aux ; true
	latex ${NAME}.tex
	latex ${NAME}.tex
	dvips ${NAME}.dvi -o ${NAME}.ps
	ps2pdf ${NAME}.ps

pdflatex: ${NAME}.tex ${GRAPHS} ${FILES} ${REFS}
	pdflatex ${NAME}
	egrep "^[^%]*\\\\makeindex" ${NAME}.tex && makeindex ${NAME}.tex ; true
	egrep "^[^%]*\\\\bibliography" ${NAME}.tex && bibtex ${NAME}.aux ; true
	pdflatex ${NAME}
	pdflatex ${NAME}

xelatex: ${NAME}.tex ${GRAPHS} ${FILES} ${REFS}
	xelatex ${NAME}
	egrep "^[^%]*\\\\makeindex" ${NAME}.tex && makeindex ${NAME}.tex ; true
	egrep "^[^%]*\\\\bibliography" ${NAME}.tex && bibtex ${NAME}.aux ; true
	xelatex ${NAME}
	xelatex ${NAME}

clean:
	rm -f ${NAME}.dvi *.bbl *.aux *.synctex.gz \
	*.log *.blg *.ascii *.out *.toc *~

clean-all: clean
	rm -f ${NAME}.pdf ${NAME}.ps

