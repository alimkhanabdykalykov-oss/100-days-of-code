import numpy as np
import re

def valid_input(label):
    """"Function that separates and checks if an input is valid: only contains 3 inputs, is either a number, number*i or i"""

    #Pattern to match number format for both real and complex numbers
    pattern=r"^[+-]?(\d+(?:\.\d+)?)?([+-](\d+(?:\.\d+)?)?i|i)?$"
    while True:
        inp= input(f"Enter the 3 coordinates for vector {label} (e.g., 1,2,3):").split(",")




        if len(inp) !=3:   #Check if only 3 coordinates are entered
            print("Error: enter only 3 coordinates")
            continue
        if all(re.match(pattern,val.strip()) for val in inp):  #Check if input matches required format
            return inp
        else:
            print("Error: invalid format, use only real or complex numbers")


def complex_converter(s):
    """Convert a string component a Python readable complex number"""
    s = s.strip()

    #convert all types of entries for complex numbers to Python readable (aka i->j)
    s = re.sub(r'(?<![0-9])i', 'j', s)


    s = re.sub(r'([0-9])i', r'\1j', s)


    s = re.sub(r'^([+-]?)j$', r'\g<1>1j', s)


    s = re.sub(r'([+-])j', r'\g<1>1j', s)

    return complex(s)

u_str= valid_input("u")
v_str= valid_input("v")

#Convert strings into numpy arrays
u=np.array([complex_converter(a) for a in u_str])
v=np.array([complex_converter(a) for a in v_str])


def cross(u, v):
    """Compute the cross product (I know numpy has is as np.cross, but I was curious to make it myself"""
    return np.array([
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0]
    ])

def back_to_complex(x):
    """Format a complex number replacing j with i for display."""

    return str(x).replace('j', 'i')

def format_answer(k):
    """Format a complex vector for display."""

    components = ', '.join(back_to_complex(x) for x in k)

    return f"[{components}]"

print(f"Cross product of 2 vectors is {format_answer(cross(u, v))}")
