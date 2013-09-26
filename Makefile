all: haskell python cpp java

haskell:
	ghc -o washing-machine-haskell main.hs
	rm --force main.hi main.o

python:
	cp main.py washing-machine-python
	chmod u+x washing-machine-python

cpp:
	g++ -o washing-machine-cpp main.cpp

java:
	javac Main.java
	echo "Main-Class: Main" > MANIFEST.MF
	jar -cmf MANIFEST.MF washing-machine-java .
	chmod u+x washing-machine-java
	rm Main.class MANIFEST.MF

clean:
	rm --force washing-machine-*
