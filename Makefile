
SOURCE=http_rendering.tex

all:
	pdflatex ${SOURCE}
	# bibtex
	# run pdflatex twice...

show: all
	evince *.pdf

show-mac: all
	open *.pdf

clean:
	rm -rf *.toc *.log *.pdf *.aux
