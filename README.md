# ifs_pascal

It has been observed that when the entries in Pascal's Triangle are reduced
modulo 2, and 0's and 1's are colored differently, the Sierpinski
Gasket emerges. 

The code in this repository allows us to investigate the patterns that are produced when 
Pascal's Triangle is reduced modulo an arbitrary integer m.

I have noticed the pattern that for all prime moduli m, Pascal's Triangle reduces to an m-row Sierpinski Gasket. 
The goal is to come up with a general iterated function system (IFS) whose attractor is Pascal's Triangle mod m. 
