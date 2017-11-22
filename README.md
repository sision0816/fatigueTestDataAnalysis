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
correct the raw data of each parts as normal way
## 2. Binding parts
Binding each corrected parts together via "partsBinding_interrupedExpParts.py"
firstly, run the "partsBinding_interrupedExpParts.py" file; secondly, call the partsBinding(n) function, n is the number of parts; thirdly, type in the parts name and output file name
## 3. Filter Max Min
Note: the initial strain should be the first data of strain without correction
## 4. Mechanical parameter analysis
as normal
## 5. Strain enenergy calculation
as normal

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
