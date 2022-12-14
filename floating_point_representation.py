# -*- coding: utf-8 -*-
"""20301207_Niloy_07_Floating_Point_Representation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18MQY7Ub45O9c4nHdIYgpOCmX8s8l4WOe

Make sure you remove `raise NotImplementedError()` and fill in any place that says `# YOUR CODE HERE`, as well as your `NAME`, `ID`, and `LAB_SECTION` below:
"""

NAME = "Soumik Deb Niloy"
ID = "20301207"
SECTION = "07"

"""---

# Floating Point Representation

## 8 bit Floating Point Representation

We will implement an 8 bit Floating point number system in this part, where First bit is a sign bit, next three bits are exponents,
and the rest 4 bits are mantissas (significands).

Numbers are divided into two categories: normals and subnormals.

For normals the encoding is:
\begin{equation}
(-1)^{sign} \times 2^{(e-3)} \times 1.fraction
\end{equation}
For subnormals the encoding is:
\begin{equation}
(-1)^{sign} \times 2^{(1-3)} \times 0.fraction
\end{equation}

Example:
\begin{aligned}
    0 001 0000 &= 2^{(1-3)} \times 1.0 = 0.25\\
    0 010 0000 &= 2^{(2-3)} \times 1.0 = 0.5\\
    0 011 0000 &= 2^{(3-3)} \times 1.0 = 1.0\\
    0 011 0100 &= 2^{(3-3)} \times 1.25 = 1.25
\end{aligned}

If the exponent is 0 then the number is considered subnormal.

Example:
\begin{aligned}
    0 000 0000 &= 2^{-2} \times 0   = 0.0\\
    0 000 1000 &= 2^{-2} \times 0.5 = 0.125\\
    0 000 1100 &= 2^{-2} \times 0.75 = 0.1875
\end{aligned}

If the exponent is 7 then and mantissa is zero then the number is 
considered infinity (inf), otherwise it is not-a-number (nan).

Example:
\begin{aligned}
    0 111 0000 &= +\infty\\
    1 111 0000 &= -\infty\\
    X 111 XXXX &= NaN
\end{aligned}

### Instructions
In this task, you need to implement the `Float8()` class. Some parts of the class are already written for you. You only need to modify `__init__(self, bitstring)` and `calculate_value(self)` fuctions, where it says `# YOUR CODE HERE`. You may ignore `raise NotImplementedError()`.
"""

import math
import itertools
import matplotlib.pyplot as plt

class Float8():
    def __init__(self, bitstring):
        assert(len(bitstring)==8)
        self.sign = bitstring[0]
        self.exponent = bitstring[1:4]
        self.mantissa = bitstring[4:]
        self.val = self.calculate_value()
        
    def __str__(self):
        return f'Sign bit value: {self.sign}\n' + \
            f'Exponent value: {self.exponent}\n' + \
            f'Mantissa value: {self.mantissa}\n' + \
            f'Floating value: {self.val}\n'
    
    def tobitstring(self):
        return self.sign + self.exponent + self.mantissa
    
    def toformattedstring(self):
        return ' '.join([self.sign, self.exponent, self.mantissa])
    
    def calculate_value(self):
        val = 0.0
        
        if self.exponent=="111":
            if self.mantissa=="0000":
                if self.sign=="0":
                    val='inf'
                else:
                    val="-inf"
            else:
                val='nan'
        elif self.exponent=="000":
            for i, bit in enumerate(self.mantissa):
                if bit=="1":
                    val = val + (2**((i+1)*(-1)))
            val = val * ((-1)**int(self.sign)) * (2**(-2))
        else:
            val = 1.0
            exponent = 0
            for i, bit in enumerate(self.mantissa):
                if bit=="1":
                    val+=(2**((i+1)*(-1)))
            for i, bit in enumerate(self.exponent[::-1]):
                if bit=="1":
                    exponent = exponent + 2**(i)
            val = val * ((-1)**int(self.sign)) * (2**(exponent-3))

        return val

'''27 test cases for 8-bit floating points'''
import numpy as np

data = [ '00000000', '00000001', '00001001', '00010000',
         '00010001', '00011000', '00011011', '00100000',
         '00101101', '00110000', '00110101', '01000011',
         '01000000', '01010000', '01011100', '01100000',
         '01110111', '01110000', '10000000', '10000001',
         '11110001', '11110000', '10110001', '10111101',
         '11100000', '11101011', '11010000']
results = ['(0, 1)', '(1, 64)', '(9, 64)', '(1, 4)', '(17, 64)', '(3, 8)', '(27, 64)',
          '(1, 2)', '(29, 32)', '(1, 1)', '(21, 16)', '(19, 8)', '(2, 1)', '(4, 1)',
          '(7, 1)', '(8, 1)', 'nan', 'inf', '(0, 1)', '(-1, 64)', 'nan', '-inf',
          '(-17, 16)', '(-29, 16)', '(-8, 1)', '(-27, 2)', '(-4, 1)']

test = [Float8(x).val for x in data]

for index in range(len(test)):
    d = test[index]
    try:
        test[index] = str(d.as_integer_ratio())
    except Exception:
        test[index] = str(d)

np.testing.assert_equal(np.array(test), np.array(results))
print('27 out of 27 outputs matched for 8-bit floating points')

"""## 16 Bit Floating Point Representation

Over here, we will implement a 16 bit Floating point number system,
where the first bit is a sign bit, next four bits are exponents,
and the rest 11 bits are mantissas (significands).

Numbers are divided into two categories: normals and subnormals.

For normals the encoding is:
\begin{equation}
(-1)^{sign} \times 2^{(e-7)} \times 1.fraction
\end{equation}
For subnormals the encoding is:
\begin{equation}
(-1)^{sign} \times 2^{(1-7)} \times 0.fraction
\end{equation}

Example:
\begin{aligned}
    0 0101 00000000000 &= 2^{(5-7)} \times 1.0  = 0.25\\
    0 0110 00000000000 &= 2^{(6-7)} \times 1.0  = 0.5\\
    0 0111 00000000000 &= 2^{(3-7)} \times 1.0  = 1.0\\
    0 0111 01000000000 &= 2^{(3-7)} \times 1.25 = 1.25
\end{aligned}

If the exponent is 0 then the number is considered subnormal.

Example:
\begin{aligned}
    0 0000 00000000000 &= 2^{-6} \times 0    = +0.0\\
    0 0000 10000000000 &= 2^{-6} \times 0.5  = +0.0078125\\
    0 0000 11000000000 &= 2^{-6} \times 0.75 = +0.01171875
\end{aligned}

If the exponent is 15 (all 1's) then and mantissa is zero then the number is considered infinity (inf), otherwise it is not-a-number (nan).
    
Example:
\begin{aligned}
    0 1111 00000000000 &= +\infty\\
    1 1111 00000000000 &= -\infty\\
    X 1111 XXXXXXXXXXX &= NaN
\end{aligned}

### Instructions
In this task, you need to implement the `Float16()` class. Some parts of the class are already written for you. You only need to modify `__init__(self, bitstring)` and `calculate_value(self)` fuctions, where it says `# YOUR CODE HERE`. You may ignore `raise NotImplementedError()`.
"""

class Float16():
    def __init__(self, bitstring):
        assert(len(bitstring)==16)
        self.sign = bitstring[0]
        self.exponent = bitstring[1:5]
        self.mantissa = bitstring[5:]
        self.val = self.calculate_value()
        
    def __str__(self):
        return f'Sign bit value: {self.sign}\n' + \
            f'Exponent value: {self.exponent}\n' + \
            f'Mantissa value: {self.mantissa}\n' + \
            f'Floating value: {self.val}\n'
    
    def tobitstring(self):
        return self.sign + self.exponent + self.mantissa
    
    def toformattedstring(self):
        return ' '.join([self.sign, self.exponent, self.mantissa])
    
    def calculate_value(self):
        val = 0.0
        
        if self.exponent=="1111":
            if self.mantissa=="00000000000":
                if self.sign=="0":
                    val='inf'
                else:
                    val="-inf"
            else:
                val='nan'
        elif self.exponent=="0000":
            for i, bit in enumerate(self.mantissa):
                if bit=="1":
                    val = val + (2**((i+1)*(-1)))
            val = val * ((-1)**int(self.sign)) * (2**(-6))
        else:
            val = 1.0
            exponent = 0
            for i, bit in enumerate(self.mantissa):
                if bit=="1":
                    val+=(2**((i+1)*(-1)))
            for i, bit in enumerate(self.exponent[::-1]):
                if bit=="1":
                    exponent = exponent + 2**(i)
            val = val * ((-1)**int(self.sign)) * (2**(exponent-7))

        return val

'''26 test cases for 16-bit floating points'''
data = [ '0011100000000010', '0100010000000000', '1100010000000000', '0100100000000000', 
         '1100100000000000', '0100101000000000', '1100101000000000', '0100110000000000', 
         '1100110000000000', '0101101110000000', '0010010000000000', '0000000000000001', 
         '0000011111111111', '0000100000000000', '0111011111111111', '0000000000000000', 
         '1000000000000000', '0111100000000000', '1111100000000000', '0111100000000001', 
         '0111110000000001', '0111111111111111', '0010101010101011', '0100010010010001', 
         '0011100000000000', '0011100000000001']
results = ['(1025, 1024)', '(3, 1)', '(-3, 1)', '(4, 1)', '(-4, 1)',
           '(5, 1)', '(-5, 1)', '(6, 1)', '(-6, 1)', '(23, 1)', '(3, 16)', '(1, 131072)',
           '(2047, 131072)', '(1, 64)', '(4095, 16)', '(0, 1)', '(0, 1)', 'inf', '-inf',
           'nan', 'nan', 'nan', '(2731, 8192)', '(3217, 1024)', '(1, 1)', '(2049, 2048)']

test = [Float16(x).val for x in data]

for index in range(len(test)):
    d = test[index]
    try:
        test[index] = str(d.as_integer_ratio())
    except Exception:
        test[index] = str(d)

np.testing.assert_equal(np.array(test), np.array(results))
print('26 out of 26 outputs matched for 16-bit floating points')
