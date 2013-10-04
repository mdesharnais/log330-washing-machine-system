all: python

python:
	cp main.py washing-machine-python
	chmod u+x washing-machine-python

clean:
	rm --force washing-machine-*
