# Intended to be run from the top level directory

# Clean log dir from previous runs
rm -rf logs/*

# Run test
bash -c "python scripts/tester.py" 2>&1 | tee /results/run.log

# Clean state
bash scripts/clean.sh

# Return stats of test for approximate analysis
python scripts/throughput.py /results/*.res 
