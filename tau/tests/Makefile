TESTERATOR = python3 -m tau.testerator

ALL = \
	m7/m7.pickle \
	m8/m8.pickle \
	m9/m9.pickle \
	m10/m10.pickle \
	m11/m11.pickle \
	m12/m12.pickle \
	project/errors.pickle \
	project/final.pickle

all: $(ALL)

m7/m7.pickle:
	cd ../..; $(TESTERATOR) create --function run_binding --compare test_binding --text --output tau/tests/$@ tau/tests/m7/*.tau tau/tests/m6/*/*/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

m8/m8.pickle:
	cd ../..; $(TESTERATOR) create --function run_typecheck --compare test_typecheck --text --output tau/tests/$@ tau/tests/m7/*.tau tau/tests/m6/*/*/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

m9/m9.pickle:
	cd ../..; $(TESTERATOR) create --function run_offsets --compare test_offsets --text --output tau/tests/$@ tau/tests/m9/*/*/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

m10/m10.pickle:
	cd ../..; $(TESTERATOR) create --function run_codegen --compare test_codegen --text --output tau/tests/$@ tau/tests/m10/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

m11/m11.pickle:
	cd ../..; $(TESTERATOR) create --function run_codegen --compare test_codegen --text --output tau/tests/$@ tau/tests/m11/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

m12/m12.pickle:
	cd ../..; $(TESTERATOR) create --function run_codegen --compare test_codegen --text --output tau/tests/$@ tau/tests/m12/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

project/errors.pickle:
	cd ../..; $(TESTERATOR) create --function run_errors --compare test_errors --text --output tau/tests/$@ tau/tests/project/error_test_cases/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

project/final.pickle:
	cd ../..; $(TESTERATOR) create --function run_codegen --compare test_codegen --text --output tau/tests/$@ tau/tests/project/final_testcases/*/*.tau
	cd ../..; $(TESTERATOR) run tau/tests/$@ 

clean:
	rm -f $(ALL)