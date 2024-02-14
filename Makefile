SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile 


%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

bib:
	wget https://researchr.org/downloadbibtex/bibliography/metaborg-spoofax -O source/bib/spoofax-raw.bib
	sed "s/http(s?):\\/\\/doi\\.acm\\.org\\///" source/bib/spoofax-raw.bib | sed "s/http(s?):\\/\\/dx\\.doi\\.org\\///" > source/bib/spoofax.bib

	