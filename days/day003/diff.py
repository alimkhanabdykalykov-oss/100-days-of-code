import re
import numpy as np
import sympy


def input_numbers(label, order):
    """
    function that separates and checks if an input is valid
    """

    #pattern from regex for inputs
    pattern = r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$"

    #number of constants in differential equation is n+1, where n is the order of differential equation


    num_constants = order + 1

    if order == 1:
        ans = f"Enter {num_constants} constants for {label} in the form a(y') + b(y) = f(t)  (e.g. a,b): "
    else:
        ans = f"Enter {num_constants} constants for {label} in the form a(y'') + b(y') + c(y) = f(t)  (e.g. a,b,c): "

    while True:
        inp = input(ans).split(",")

        if len(inp) != num_constants:
            print(f"Error: enter exactly {num_constants} constants for a {order}-order equation")
            continue

        if all(re.match(pattern, val.strip()) for val in inp):
            return [float(val.strip()) for val in inp]  # Return as floats, not strings
        else:
            print("Error: invalid format, use only real numbers")


def choose_order():
    """
    let the user pick equation order
    """
    while True:

        choice = input("Solve a (1) first-order or (2) second-order ODE? Enter 1 or 2: ").strip()

        if choice in ("1", "2"):
            return int(choice)
        print("Error: enter 1 or 2")


def input_forcing(label):
    """
    ask the user for the right-hand side f(t) of the ODE
    """
    t = sympy.Symbol("t")

    names = {
        "t":   t,
        "sin": sympy.sin,
        "cos": sympy.cos,
        "exp": sympy.exp,
        "tan": sympy.tan,
        "ln":  sympy.ln,
        "log": sympy.ln,
        "sqrt":sympy.sqrt,
        "pi":  sympy.pi,
        "E":   sympy.E,
    }

    print(f"\nEnter the right-hand side f(t) for {label}")
    print("  Examples: 0,  2*sin(3*t),  exp(2*t),  t**2 + 1,  cos(t)*exp(-t)")
    print("  Use ^ or ** for powers - both work")

    while True:


        raw = input("  f(t) = ").strip()
        raw = raw.replace("^", "**")

        try:

            expr = sympy.sympify(raw, locals=names)
            return expr


        except sympy.core.sympify.SympifyError:
            print("  Error: could not parse that expression, try again")


def odes(order, constants, forcing):
    """
    combine the constants and forcing function into a sympy ade equation
    """

    t = sympy.Symbol("t")
    y = sympy.Function("y")

    if order == 1:


        a, b = constants
        ode = sympy.Eq(a * y(t).diff(t) + b * y(t), forcing)

    else:


        a, b, c = constants
        ode = sympy.Eq(a * y(t).diff(t, 2) + b * y(t).diff(t) + c * y(t), forcing)

    return ode



def input_initial_conditions(order):

    """
    optionally collect initial conditions from the user
    """


    t = sympy.Symbol("t")
    y = sympy.Function("y")

    while True:


        choice = input("\nDo you want to enter initial conditions? (yes/no): ").strip().lower()
        if choice in ("yes", "no"):
            break
        print("  Error: please type yes or no")



    if choice == "no":
        return None

    ics = {}

    try:
        t0  = float(input("  t₀ = ").strip())
        y0  = float(input("  y(t₀) = ").strip())


        ics[y(t0)] = y0

        if order == 2:

            yp0 = float(input("  y'(t₀) = ").strip())
            ics[y(t).diff(t).subs(t, t0)] = yp0

    except ValueError:

        print("  Error: initial conditions must be plain numbers — skipping them")
        return None

    return ics


def solve(order, ode, ics):



    """
    solve the ODE and print the result.
    """

    t = sympy.Symbol("t")
    y = sympy.Function("y")

    print("\nSolving")

    try:
        solution = sympy.dsolve(ode, y(t), ics=ics)

    except NotImplementedError:
        print("Error: SymPy could not solve this ODE analytically")
        return

    except Exception as e:
        print(f"Error: {e}")
        return

    print("\nSolution:")
    sympy.pprint(solution)
    print(f"\nLaTeX: {sympy.latex(solution)}")




print("ODE Calculator")
print("-" * 30)

order      = choose_order()
constants  = input_numbers("your equation", order)
forcing    = input_forcing("your equation")
ode        = odes(order, constants, forcing)
ics        = input_initial_conditions(order)

solve(order, ode, ics)
