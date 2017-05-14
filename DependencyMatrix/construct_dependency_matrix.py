import numpy as np

block = 32

def xor(sub1,sub2):
    n = sub1.shape[1]
    total = np.concatenate((sub1,sub2),axis = 1)
    to_mult = np.concatenate((np.identity(n),np.identity(n)),axis = 0)
    return np.dot(total,to_mult)

def make_matr_G(r):
    res = np.zeros((block,block))
    shift = np.zeros((block,block))
    quort = block/4
    for i in range(block):
        for j in range(block):
            if i // quort == j // quort:
                res[i][j] = 0.5
            if (i+r) % block == j:
                shift[i][j] = 1
    return np.dot(res,shift)

def makeG(sub, r):
    r = make_matr_G(r)
    return np.dot(sub,r)

def um(m):
    res = np.zeros((m,m))
    for i in range(m):
        for j in range(i,m):
            res[i][j] = 2**(i-j)
    return res

def plus(sub1,sub2):
    total = np.concatenate((sub1,sub2),axis = 1)
    n = sub1.shape[1]
    to_mult = np.concatenate((um(n),um(n)),axis = 0)
    return np.dot(total,to_mult)

def swap(block1, block2):
    return block2, block1


if __name__ == "__main__":
    test = np.array([[1 if i == j else 0 for j in range(4*block)] 
                      for i in range(4*block)])
    a = test[:,:block]
    b = test[:,block:2*block]
    c = test[:, 2*block:3*block]
    d = test[:, 3*block:4*block]

    b = xor(b, makeG(a, 5))
    c = xor(c, makeG(d,21))
    a = plus(a, makeG(b,13))
    e = makeG(plus(b,c),21)
    b = plus(b,e)
    c = plus(c,e)
    d = plus(d, makeG(c,13))
    b = xor(b, makeG(a, 21))
    c = xor(c, makeG(d,5))
    [a,b] = swap(a,b)
    [c,d] = swap(c,d)
    [b,c] = swap(b,c)
    test = np.concatenate((b,d,a,c), axis=1)

    f = open('belt.txt', 'w')
    for i in range(4*block):
        toPrint = ""
        for j in range(4*block):
            toPrint += str(test[i][j]) + " "
        print(toPrint,file = f)
    f.close()
