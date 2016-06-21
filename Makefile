.PHONY: test

test:
	py.test

verbose:
	py.test -v

c:
	gcc -shared -o testlib.o -fPIC testlib.c
