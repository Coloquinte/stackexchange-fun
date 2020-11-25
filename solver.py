
import random
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

def check_problem(n, l, u):
    assert len(l) == n
    assert len(u) == n
    for lb, ub in zip(l, u):
        assert lb <= ub

def check_solution(n, l, u, x, tol=1.0e-12):
    check_problem(n, l, u)
    for i in range(n):
        assert x[i] >= l[i] - tol
        assert x[i] <= u[i] + tol
        if i == 0:
            avg = x[1]
        elif i == n-1:
            avg = x[n-2]
        else:
            avg = 0.5 * (x[i-1] + x[i+1])
        if x[i] <= l[i] + tol:
            assert x[i] >= avg - tol
        elif x[i] >= u[i] - tol:
            assert x[i] <= avg + tol
        else:
            assert abs(x[i] - avg) <= tol

def random_problem(n):
    l = [0.0 for i in range(n)]
    u = [0.0 for i in range(n)]
    for i in range(n):
        a = random.random()
        b = random.random()
        l[i] = min(a, b)
        u[i] = max(a, b)
    return (l, u)

def find_first_breakpoint(n, l, u):
    """
    Find the first point where the solution departs from a constant line
    """
    lb = -float("inf")
    ub = float("inf")
    lb_ind = -1
    ub_ind = -1
    for i in range(n):
        new_lb = l[i]
        new_ub = u[i]
        assert new_lb <= new_ub
        if new_lb > ub:
            return ub_ind, ub
        if new_ub < lb:
            return lb_ind, lb
        if new_ub < ub:
            ub_ind = i
            ub = new_ub
        if new_lb > lb:
            lb_ind = i
            lb = new_lb
    # No breakpoint found: the optimal solution is a straight line
    return n-1, 0.5 * (lb + ub)

def find_last_breakpoint(n, l, u):
    """
    Find the point where the solution returns to a constant line
    """
    k, val = find_first_breakpoint(n, list(reversed(l)), list(reversed(u)))
    return n-1-k, val

def find_next_breakpoint(n, l, u, bp, bp_val, last_bp, last_bp_val):
    """
    Find the next breakpoint in the solution
    """
    lb_slope = -float("inf")
    ub_slope = float("inf")
    l_bp_ind = -1
    u_bp_ind = -1
    for i in range(bp+1, last_bp+1):
        lb = l[i] if i != last_bp else last_bp_val
        ub = u[i] if i != last_bp else last_bp_val
        new_lb_slope = (lb - bp_val) / (i-bp)
        new_ub_slope = (ub - bp_val) / (i-bp)
        if new_lb_slope > ub_slope:
            return u_bp_ind, u[u_bp_ind]
        if new_ub_slope < lb_slope:
            return l_bp_ind, l[l_bp_ind]
        if new_ub_slope < ub_slope:
            u_bp_ind = i
            ub_slope = new_ub_slope
        if new_lb_slope > lb_slope:
            l_bp_ind = i
            lb_slope = new_lb_slope
    # No breakpoint found: the solution will go back to a straight line at the last breakpoint
    return last_bp, last_bp_val

def solve_core(n, l, u):
    x = [None for i in range(n)]
    first_bp, first_bp_val = find_first_breakpoint(n, l, u)
    for i in range(first_bp+1):
        x[i] = first_bp_val
    if first_bp == n-1:
        return x
    last_bp, last_bp_val = find_last_breakpoint(n, l, u)
    for i in range(last_bp, n):
        x[i] = last_bp_val
    bp = first_bp
    bp_val = first_bp_val
    while bp < last_bp:
        next_bp, next_bp_val = find_next_breakpoint(n, l, u, bp, bp_val, last_bp, last_bp_val)
        for i in range(bp+1, next_bp+1):
            x[i] = ((next_bp - i) * bp_val + (i - bp) * next_bp_val) / (next_bp - bp)
        bp = next_bp
        bp_val = next_bp_val
    return x

def solve(n, l, u):
    check_problem(n, l, u)
    x = solve_core(n, l, u)
    check_solution(n, l, u, x)
    return x

def draw_problem(n, l, u, x):
    for i in range(n):
        plt.plot([i, i], [l[i], u[i]], color='black')
    plt.gca().get_yaxis().set_visible(False)
    plt.show()
    for i in range(n):
        plt.plot([i, i], [l[i], u[i]], color='black')
    plt.gca().get_yaxis().set_visible(False)
    plt.plot(x, color='red', marker='o')
    plt.show()

n = 11
for i in range(10):
    l, u = random_problem(n)
    x = solve(n, l, u)
    draw_problem(n, l, u, x)
