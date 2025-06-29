def trapezoidal(x, a, b, c, d):
    if x <= a or d <= x:
        return 0
    elif a <= x <= b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c <= x <= d:
        return (d - x) / (d - c)


def triangular(x, a, b, c):
    if x<=a:
        return 0
    elif a<=x<=b:
        return (x-a)/(b-a)
    elif b<=x<=c:
        return (c-x)/(c-b)
    else:
        return 0 