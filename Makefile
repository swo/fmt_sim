.PHONY: test

test:
	py.test

verbose:
	py.test -v

c:
	gcc -O3 -shared -o bayesian_lib.o -fPIC bayesian_lib.c
