all: joe.dimacs
	@echo "Done."

joe.dimacs:
	./randomSAT.py -o joe.dimacs

clean:
	$(RM) -rf joe.dimacs
	$(RM) -rf *.pyc
