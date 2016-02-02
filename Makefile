PYTHON ?= python

ifeq ($(VERBOSE),1)
  Verb := 
else
  Verb := @
endif

.PHONY: check-svcb

check-svcb:
	$(Verb)$(PYTHON) -m unittest discover
