NOTEBOOK_DIR ?= .
NOTEBOOK_NAMES := sc1.ipynb sc2.ipynb sc3.ipynb sc4.ipynb sc5.ipynb sc6.ipynb sc7.ipynb
NOTEBOOKS := $(addprefix $(NOTEBOOK_DIR)/,$(NOTEBOOK_NAMES))
PDFS := $(NOTEBOOKS:.ipynb=.pdf)

NBCONVERT := jupyter nbconvert
NBCONVERT_OPTIONS := --to latex --template latex_minted --output-dir=$(NOTEBOOK_DIR)

UPLATEX := uplatex
UPLATEX_OPTIONS := -shell-escape -interaction=nonstopmode -output-directory=$(NOTEBOOK_DIR)

DVIPDFMX := dvipdfmx
DVIPDFMX_OPTIONS := -p 260mm,348mm

.PHONY: all clean

all: $(PDFS)

%.pdf: %.ipynb
	$(NBCONVERT) $(NBCONVERT_OPTIONS) $<
	sed -i '' \
		's/\\documentclass\[11pt,dvipdfmx\]{jsarticle}/\\documentclass[uplatex,dvipdfmx,tombow]{jsbook}/' \
		$*.tex
	$(UPLATEX) $(UPLATEX_OPTIONS) $*.tex
	$(DVIPDFMX) $(DVIPDFMX_OPTIONS) -o $@ $*.dvi

clean:
	$(RM) \
		$(NOTEBOOKS:.ipynb=.tex) \
		$(NOTEBOOKS:.ipynb=.dvi) \
		$(NOTEBOOKS:.ipynb=.aux) \
		$(NOTEBOOKS:.ipynb=.log) \
		$(NOTEBOOKS:.ipynb=.out) \
		$(NOTEBOOKS:.ipynb=.toc) \
		$(NOTEBOOKS:.ipynb=.synctex.gz) \
		$(NOTEBOOKS:.ipynb=.fls) \
		$(NOTEBOOKS:.ipynb=.fdb_latexmk)

	$(RM) -r _minted/ \
		$(NOTEBOOKS:.ipynb=_files)
