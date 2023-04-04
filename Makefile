# Makefile for the CS:APP Shell Lab

TEAM = NOBODY
DRIVER = ./sdriver.pl
TSH = ./tsh
TSHREF = ./tshref
TSHARGS = "-p"
CC = gcc
CXX = g++

##
## Compile with no optimization because we don't care about performance and want to simplify debugging
##
CFLAGS = -Wall -O -g
CXXFLAGS=$(CFLAGS)
FILES = ./myspin ./mysplit ./mystop ./myint

all: $(FILES) tsh

tsh: tsh.o jobs.o helper-routines.o
	$(CXX) -o tsh tsh.o jobs.o helper-routines.o

##################
# Regression tests
##################

tests: tsh test01 test02 test03 test04 test05 test06 test07 test08 test09 test10 test11 test12 test13 test14 test15 test16
	@echo all time


# Run tests using the student's shell program
test01: tsh $(FILES)
	$(DRIVER) -t trace01.txt -s $(TSH) -a $(TSHARGS)
test02: tsh $(FILES)
	$(DRIVER) -t trace02.txt -s $(TSH) -a $(TSHARGS)
test03: tsh $(FILES)
	$(DRIVER) -t trace03.txt -s $(TSH) -a $(TSHARGS)
test04: tsh $(FILES)
	$(DRIVER) -t trace04.txt -s $(TSH) -a $(TSHARGS)
test05: tsh $(FILES)
	$(DRIVER) -t trace05.txt -s $(TSH) -a $(TSHARGS)
test06: tsh $(FILES)
	$(DRIVER) -t trace06.txt -s $(TSH) -a $(TSHARGS)
test07: tsh $(FILES)
	$(DRIVER) -t trace07.txt -s $(TSH) -a $(TSHARGS)
test08: tsh $(FILES)
	$(DRIVER) -t trace08.txt -s $(TSH) -a $(TSHARGS)
test09: tsh $(FILES)
	$(DRIVER) -t trace09.txt -s $(TSH) -a $(TSHARGS)
test10: tsh $(FILES)
	$(DRIVER) -t trace10.txt -s $(TSH) -a $(TSHARGS)
test11: tsh $(FILES)
	$(DRIVER) -t trace11.txt -s $(TSH) -a $(TSHARGS)
test12: tsh $(FILES)
	$(DRIVER) -t trace12.txt -s $(TSH) -a $(TSHARGS)
test13: tsh $(FILES)
	$(DRIVER) -t trace13.txt -s $(TSH) -a $(TSHARGS)
test14: tsh $(FILES)
	$(DRIVER) -t trace14.txt -s $(TSH) -a $(TSHARGS)
test15: tsh $(FILES)
	$(DRIVER) -t trace15.txt -s $(TSH) -a $(TSHARGS)
test16: tsh $(FILES)
	$(DRIVER) -t trace16.txt -s $(TSH) -a $(TSHARGS)

# Run the tests using the reference shell program
rtests: $(TSHREF) rtest01 rtest02 rtest03 rtest04 rtest05 rtest06 rtest07 rtest08 rtest09 rtest10 rtest11 rtest12 rtest13 rtest14 rtest15 rtest16
	@echo all time
rtest01: $(TSHREF) $(FILES)
	$(DRIVER) -t trace01.txt -s $(TSHREF) -a $(TSHARGS)
rtest02: $(TSHREF) $(FILES)
	$(DRIVER) -t trace02.txt -s $(TSHREF) -a $(TSHARGS)
rtest03: $(TSHREF) $(FILES)
	$(DRIVER) -t trace03.txt -s $(TSHREF) -a $(TSHARGS)
rtest04: $(TSHREF) $(FILES)
	$(DRIVER) -t trace04.txt -s $(TSHREF) -a $(TSHARGS)
rtest05: $(TSHREF) $(FILES)
	$(DRIVER) -t trace05.txt -s $(TSHREF) -a $(TSHARGS)
rtest06: $(TSHREF) $(FILES)
	$(DRIVER) -t trace06.txt -s $(TSHREF) -a $(TSHARGS)
rtest07: $(TSHREF) $(FILES)
	$(DRIVER) -t trace07.txt -s $(TSHREF) -a $(TSHARGS)
rtest08: $(TSHREF) $(FILES)
	$(DRIVER) -t trace08.txt -s $(TSHREF) -a $(TSHARGS)
rtest09: $(TSHREF) $(FILES)
	$(DRIVER) -t trace09.txt -s $(TSHREF) -a $(TSHARGS)
rtest10: $(TSHREF) $(FILES)
	$(DRIVER) -t trace10.txt -s $(TSHREF) -a $(TSHARGS)
rtest11: $(TSHREF) $(FILES)
	$(DRIVER) -t trace11.txt -s $(TSHREF) -a $(TSHARGS)
rtest12: $(TSHREF) $(FILES)
	$(DRIVER) -t trace12.txt -s $(TSHREF) -a $(TSHARGS)
rtest13: $(TSHREF) $(FILES)
	$(DRIVER) -t trace13.txt -s $(TSHREF) -a $(TSHARGS)
rtest14: $(TSHREF) $(FILES)
	$(DRIVER) -t trace14.txt -s $(TSHREF) -a $(TSHARGS)
rtest15: $(TSHREF) $(FILES)
	$(DRIVER) -t trace15.txt -s $(TSHREF) -a $(TSHARGS)
rtest16: $(TSHREF) $(FILES)
	$(DRIVER) -t trace16.txt -s $(TSHREF) -a $(TSHARGS)


# clean up
clean:
	rm -f $(FILES) *.o *~
