def block0(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 10
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 13
    y *= x
    z += y
    return z
def block1(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 13
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    return z
def block2(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 13
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 3
    y *= x
    z += y
    return z
def block3(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -11
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 1
    y *= x
    z += y
    return z
def block4(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 11
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 9
    y *= x
    z += y
    return z
def block5(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -4
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 3
    y *= x
    z += y
    return z
def block6(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 12
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 5
    y *= x
    z += y
    return z
def block7(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 12
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 1
    y *= x
    z += y
    return z
def block8(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 15
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 0
    y *= x
    z += y
    return z
def block9(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -2
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 13
    y *= x
    z += y
    return z
def block10(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -5
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 7
    y *= x
    z += y
    return z
def block11(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -11
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return z
def block12(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -13
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 12
    y *= x
    z += y
    return z
def block13(w=0,x=0,y=0,z=0):
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -10
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 8
    y *= x
    z += y
    return z
blocks = {0: block0,1:block1,2:block2,3:block3,4:block4,5:block5,6:block6,7:block7,8:block8,9:block9,10:block10,11:block11,12:block12,13:block13}

def python_block(i,w=0,x=0,y=0,z=0):
    return blocks[i](w,x,y,z)
