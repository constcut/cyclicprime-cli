# Cyclic prime numbers console line interface

This small aplication used to generate cyclic prime numbers from console interface

Usage: python cyclicprime.py (-prime prime_number | -number number) numeric_system max_digits


## Example 1

When you run the command 'python cyclicprime.py -prime 7 10 100'

You would get the folowing output:

For the prime number 7 in numeric system 10 we got cyclic number 285714  that is
  1.0 reptend level

Period 6

2  in decimal is  2

5  in decimal is  5

7  in decimal is  7

71  in decimal is  71

571  in decimal is  571

857  in decimal is  857

2857  in decimal is  2857

28571  in decimal is  28571

1428571  in decimal is  1428571

71428571  in decimal is  71428571

7142857142857  in decimal is  7142857142857

... and many more lines


## Example 2

When you run the command 'python cyclicprime.py -number 142857 10 100'

You would get the folowing output:

2  in decimal is  2

5  in decimal is  5

7  in decimal is  7

71  in decimal is  71

571  in decimal is  571

857  in decimal is  857

2857  in decimal is  2857

28571  in decimal is  28571

1428571  in decimal is  1428571

71428571  in decimal is  71428571

7142857142857  in decimal is  7142857142857

571428571428571  in decimal is  571428571428571

... and some more lines


## Requirements

```
pip install gmpy2
pip install factordb-pycli
```

You may epxerience issue of installing gmpy2 on windows, in this case you may use unofficial wheel:
https://www.lfd.uci.edu/~gohlke/pythonlibs/
