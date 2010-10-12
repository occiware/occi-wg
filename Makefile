
HTTP=http_rendering.tex
INFRA=infrastructure.tex

all:
	pdflatex ${HTTP}
	pdflatex ${INFRA}
	# bibtex
	# run pdflatex twice...

show: all
	evince *.pdf

show-mac: all
	open *.pdf

clean:
	rm -rf *.toc *.log *.pdf *.aux
