def  mergeStrings(a, b):
    a = list(a)
    b = list(b)
    al = len(a)
    bl = len(b)
    minl = min(al,bl)
    maxl = max(al,bl)
    result = ''
    for i in range(minl):
        result += a[i] + b[i]
    if minl == len(a):
        result += b[minl:]
    else:
        result += a[minl:]
    print(result)

a = 'abc'
b = 'def'

mergeStrings(a, b)