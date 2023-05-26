MILESTONES = \
	milestone02-3.pdf

all: language.pdf $(MILESTONES)

%.pdf : %.md
	pandoc -o $@ $< 

%.html : %.md
	pandoc -o $@ $< 
