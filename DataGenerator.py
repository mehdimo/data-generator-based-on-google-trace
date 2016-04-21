# This code preprocess Google Trace files to generate a specific dataset for IoT simulations.
# Developed by: Mehdi Mohammadi, Western Michigan University

import sys
import Preprocess

def main():
    # This code just processes 'Task Events' tables to generate data.
    # You need to give the path of the google trace file here. Google trace files are in the format of "part-?????-of-?????.csv". 	
    file1 = 'orig/part-00000-of-00000.csv'   
    
    proc = Preprocess.Preprocessor()
    proc.generate_data(file1)
    print("finished reading.")

if __name__  == "__main__" :
    main()