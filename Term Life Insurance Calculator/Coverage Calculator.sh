echo "Running....checking dependencies"

# Install libraries in requirements.txt
python -m pip install -r requirements.txt  #### Uncomment this line if you do not already have installed the required python packages ####

# Execute script
python module/calculate_life_coverage.py 

echo "Press "Enter" to exit"
read
read
