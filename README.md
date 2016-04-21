Data Generator based on Google Trace Dataset
================================

The dataset generated by this application is an adaptation of [google cluster trace dataset](https://github.com/google/cluster-data). We used 'task events' table as the source of requests for Auction-based IoT applications. In the processed dataset, we have the following fields separated by comma.
* Job id
* Task id; job id and task id taken directly from the original dataset. They together represent the unique requests in the system. 
* Arrival time 
* Finish time
* Delay sensitivity (ds), a number between 0 and 3 (3 means that a request is more delay sensitive). 
* Service rate (mu), assigned base on the delay sensitivity of the request and a random uniform number between -0.005 ~ 0.005.
* Number of clouds, which is picked proportional to the delay sensitivity (ds). It is a random number between 2^(ds) and 2^(ds+1).
* Payment, calculated based on the requested resource usage (cpu, memory and disk) and an approximate [standard google cloud pricing plan](https://cloud.google.com/products/calculator/).
```
    computePrice = 0.0006  // dollor per minute
    diskPrice    = 0.00015 // dollor per minute
    unitPay = computePrice * (cpuUsage + memoryUsage) + (diskPrice * diskUsage)
    payment = (1+unitPay) * (duration* mu * N) 
```