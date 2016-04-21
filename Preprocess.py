# This code preprocess Google Trace files to generate a specific dataset for IoT simulations.
# Developed by: Mehdi Mohammadi, Western Michigan University

import sys
import os
import csv
import numpy
import math
import random

class Preprocessor:
    
    def __init__(self):
            self.dataset = {} # processed dataset

    def generate_data(self, dataFile):
        fileName = dataFile
        sys.stdout.write("Reading the files... \n")
        with open(dataFile, mode='rb') as dataFile:
            csvreader = csv.reader(dataFile, delimiter=',')
            for line in csvreader:
                key = (line[2], line[3])
                arrivalTime = 0
                finishTime = 0
                delaySensivity = line[7]
                payment = 0
                mu = 0
                N = 1
                if(line[5] == '0'):
                    arrivalTime = long(line[0])/10000000
                elif (line[5] == '4'):
                    finishTime = long(line[0])/10000000                
                if (not self.dataset.has_key(key)):
                    self.dataset.setdefault(key, (arrivalTime, finishTime, delaySensivity, payment, mu, N))
                else:
                    (arr, fin, a7, pay, mu, N) = self.dataset[key]
                    if(line[5]=='0'): # SUBMIT event activity
                        arr = arrivalTime
                    elif(line[5] == '4'): # FINISH event activity
                        fin = finishTime 
                        duration = fin - arr
                        cpuUsage = float(line[9])
                        ramUsage = float(line[10])
                        diskUsage = float(line[11])                        
                        mu = self.computeServiceRate(int(delaySensivity))
                        N = self.getCloudNumbers(a7)
                        pay = self.calculatePayment(duration, mu, N, cpuUsage, ramUsage, diskUsage)
                    self.dataset[key] = (arr, fin, a7, pay, mu, N)    
        output= fileName + "processed.csv"
        self.printCSV(output)
    
    # calculate the payment for a desired service based on the time of service and resource usage (cpu, memory and disk).
    # resource usage is normalized between [0,1] in the google-cluster data
    def calculatePayment(self, duration, mu, N, cpu, memory, disk):
        # The following unit prices for computation and disk are calculated based on google cloud pricing plan with 1 server, 10GB SSD and 100GB hard disk
        computePrice = 0.0006  # dollor per minute
        diskPrice    = 0.00015 # dollor per minute
        unitPay = computePrice * (cpu + memory) + (diskPrice * disk)
        unitPay = unitPay/60
        N=2
        payment = (1+unitPay) * (duration * mu * N)
        return payment
    
    def assignArrivalRate(self, cpuUsage):
        if(cpuUsage < 0.167):
            return 0.028
        elif(cpuUsage >= 0.167 and cpuUsage < 0.34):
            return 0.025
        else: 
            return 0.020
    
    def computeServiceRate(self, ds):
        mu = 0
        #r = random.uniform(-0.005, 0.005)
        r = random.uniform(-0.5, 0.5)
        if(ds==0):
            mu = 0.20
        elif(ds == 1):
            mu = 0.23
        elif(ds == 2):
            mu = 0.26
        elif(ds == 3):
            mu = 0.29
        mu = mu + r
        mu = abs(mu)
        mu = round(mu, ndigits=4)
        return mu
    
    # we consider number of clouds for serving a request is related to the delay sensivity (ds) of that request.    
    def getCloudNumbers(self, delaySensivity):           
        delaySensivity = int(delaySensivity)
        j = delaySensivity + 1
        r = int(math.pow(2, delaySensivity))
        s = int(math.pow(2, j))
        c = random.randint(r, s)
        return c

    def printD(self):       
        i=0
        for (key,val) in self.dataset.items():
            if(val[0]!= 0 and val[1] != 0):
                i += 1
                print key, val
        print "completed: ", i
        print "total = ", len(self.dataset)
    
    def printCSV(self, fileName):       
        with open(fileName, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            i=0
            for (key,val) in self.dataset.items():            
                if(val[0]!= 0 and val[1] != 0):
                    i += 1       
                    newVals = []
                    newVals.append(key[0])
                    newVals.append(key[1]) 
                    for vl in val:
                        newVals.append(vl)
                    
                    csvwriter.writerow(newVals)
            print "completed: ", i
            print "total = ", len(self.dataset)    