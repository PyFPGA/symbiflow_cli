# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile snippets images devices

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile snippets images
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

snippets:
	@echo "Generating $@"
	@symbiflow -h > help.txt
	@for cmd in all syn pnr bit pgm; do \
		symbiflow $$cmd -h > help-$$cmd.txt ; \
	done
	@echo "$@ generated"

images:
	make -C dot

devices:
	python3 devices.py

clean:
	rm -rf $(BUILDDIR)

clean-all: clean
	rm -f *.txt
