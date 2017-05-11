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
	wget http://researchr.org/downloadbibtex/bibliography/metaborg-spoofax -O source/spoofax-raw.bib
	sed "s/http:\\/\\/doi\\.acm\\.org\\///" source/spoofax-raw.bib | sed "s/http:\\/\\/dx\\.doi\\.org\\///"  > source/spoofax.bib