# fatigueTestDataAnalysis
# Processing data for load-controlled test
## 1. Correct the raw data
## 2. Binding parts
## 3. Filter Max Min
## 4. Mechanical parameter analysis
## 5. Strain enenergy calculation


# Processing data for strain-controlled test
## 1. Correct the raw data
"timeSequenceDataCorrector_strainControl.py", take care of the deviation shrethold value and whether has mean strain loading,
if have mean strain loading, should go to "Processing data with mean stress/strain loading"
## 2. Binding parts
## 3. Filter Max Min
## 4. Mechanical parameter analysis
## 5. Strain enenergy calculation


# Processing data for tests with interrupted recording/experiments
## 1. Correct the raw data
a. correct the raw data of each parts as normal way
b. name the output data follow "SK200_01_exp1_timeData.csv"
## 2. Binding parts
a. Binding each corrected parts together via "partsBinding_interrupedExpParts.py"
b. firstly, run the "partsBinding_interrupedExpParts.py" file; secondly, call the partsBinding(n) function, n is the number of parts; thirdly, type in the parts name and output file name
c. name the output data follow "SK200_01_timeData_binded.csv"
## 3. Filter Max Min
Note: the initial strain should be the first data of strain without correction
a. name the output data follow "SK200_01_binded_maxMinData.csv"
## 4. Mechanical parameter analysis
Note: the initial strain should be the first data of strain without correction
## 5. Strain enenergy calculation
Note: the initial strain should be the first data of strain without correction

# Processing data for tests with holding cycles
## 1. Correct the raw data
## 2. Binding parts
## 3. Filter Max Min
## 4. Mechanical parameter analysis
## 5. Strain enenergy calculation


# Processing data with mean stress/strain loading
## 1. Correct the raw data
## 2. Binding parts
## 3. Filter Max Min
## 4. Mechanical parameter analysis
## 5. Strain enenergy calculation
