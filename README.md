# Cache-Memory

Cache Memory is a high-speed memory used to reduce the average time taken to fetch data from the Main Memory. It stores a copy of the frequently used data fetched from the Main Memory.

## General Information

There are three mapping techniques used in the case of Cache Memory –

* Direct Mapping
* Associative Memory
* N – Way Set Associative Memory

All these techniques have their own pros and cons, which directly affect the time taken to fetch the requested data and the number of Cache Hits and Cache Misses encountered.

`Cache Hit` – When the requested data is found in the Cache Memory, this instance is known as Cache Hit.

`Cache Miss` – When the requested data is missing in the Cache Memory, this instance is known as Cache Miss.

`Cache Latency` – When the requested address isn’t found in the Cache Memory and the overall time taken to fetch the address is more than the time it would have taken to directly access the address from the Main Memory.

## Assumptions

Following are the assumptions considered for this program –

* All the inputs must be powers of `2`.
* The replacement policy used is `FIFO`.
* Words are represented by a string in the following format, `Words + Word Number`.
* The input address is in binary.
* Any word should not be added twice.
