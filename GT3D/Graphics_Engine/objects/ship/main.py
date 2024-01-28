with open("untitled.obj") as f:
    ls = f.read()
ls = ls.replace("s 0\n", "")
ls = ls.replace("s 1\n", "")
with open("ship.obj", "w") as o:
    o.write(ls)
