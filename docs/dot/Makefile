#!/usr/bin/make

FILES  = $(wildcard *.dot)
FILES := $(basename $(FILES))
FILES := $(addsuffix .svg,$(FILES))

ODIR = ../_static

vpath %.svg $(ODIR)

%.svg: %.dot
	@mkdir -p $(ODIR)
	dot -Tsvg $< -o $(ODIR)/$@

all: $(FILES)
