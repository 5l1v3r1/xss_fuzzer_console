.DEFAULT_GOAL := test

FILES :=            \
	attack.py  		\
	connect.py 		\
	fuzz_thread.py 	\
	intro.py		\
 	README.md 		\
	thread.py 		\
	TestFuzzer.py   \
	util.py 		\
	xsshell.py

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python2.7
    PIP      := pip2.7
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := pydoc2.7
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python2.7
    PIP      := pip2.7
    PYLINT   := pylint
    COVERAGE := coverage 
    PYDOC    := pydoc2.7
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python2.7
    PIP      := pip2.7
    PYLINT   := pylint
    COVERAGE := coverage 
    PYDOC    := pydoc2.7
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python2.7
    PIP      := pip2.7
    PYLINT   := pylint
    COVERAGE := python -m coverage
    PYDOC    := pydoc2.7
    AUTOPEP8 := autopep8
endif

.pylintrc:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@


Fuzzer.log:
	git log > Fuzzer.log

#.PHONY: RunFuzzer.tmp
#RunCollatz.tmp: .pylintrc
	#-$(PYLINT) .py
	#-$(PYLINT) RunCollatz.py
	#$(PYTHON) RunCollatz.py < RunCollatz.in > RunCollatz.tmp
	#diff RunCollatz.tmp RunCollatz.out

.PHONY: TestFuzzer.tmp
TestFuzzer.tmp: .pylintrc
	-$(PYLINT) TestFuzzer.py
	-$(COVERAGE) run    --branch TestFuzzer.py >  TestFuzzer.tmp 2>&1
	-$(COVERAGE) report -m                     >> TestFuzzer.tmp
	cat TestFuzzer.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  Fuzzer.log
	rm -f  RunFuzzer.tmp
	rm -f  TestFuzzer.tmp
	rm -rf __pycache__

format:
	
	$(AUTOPEP8) -i attack.py   
	$(AUTOPEP8) -i fuzz_thread.py  
	$(AUTOPEP8) -i TestFuzzer.py   
	$(AUTOPEP8) -i util.py
	$(AUTOPEP8) -i connect.py  
	$(AUTOPEP8) -i intro.py        
	$(AUTOPEP8) -i xsshell.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status


test: Fuzzer.log TestFuzzer.tmp
	ls -al
	make check

versions:
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	-which $(PYDOC)
	-$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	$(PIP) list


