# Importing data to the program

The $`Z^2_n`$ statistics a la Buccheri et al. 1983 takes as input the arrival times of photons detected by telescopes. Therefore the program uses as input an event file with a dataset representing these values, stored on a collum named "TIME".

| TIME |
|:----:|
|   1  |
|   2  |
|   3  |
|   4  |
|   5  |
|  ... |

The software currently supports the following file formats:

* ascii
* csv
* fits
* hdf5