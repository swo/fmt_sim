.PHONY: test

test:
	py.test

verbose:
	py.test -v

c:
	gcc -O3 -shared -o testlib.o -fPIC testlib.c
