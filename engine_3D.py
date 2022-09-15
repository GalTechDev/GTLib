import numba
from math import sqrt

A = (0.0002,100.0001,1.0002)
D = (-0.4901,0.8601,1.3001)
C = (0.0001,0.0001, 1.0001)


f=1
scall = 100 #1:100

@numba.njit()
def distance(a,b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

@numba.njit()
def vecteur(a,b):
    return ((b[0]-a[0]),(b[1]-a[1]),(b[2]-a[2]))

#@numba.njit()
def pos_on_screen(a=A,c=C,d=D):
    a=list(a).copy()
    for i in range(3):
        if a[i]==c[i] and a[i]==d[i]:
            a[i]+=0.0001
    a=(a[0],a[1], a[2])
    v_cd = vecteur(c,d)
    
    #cd = [(1/v_cd[0], -c[0]/v_cd[0]), (1/v_cd[1], -c[1]/v_cd[1]), (1/v_cd[2], -c[2]/v_cd[2])]
    #equation (cd)

    g=v_cd[0]
    h=v_cd[1]
    i=v_cd[2]
    j= -(g*d[0]+h*d[1]+i*d[2])
    #On cherche un vecteur n (a;b;c) normal au plan. cd
    #On déduit qu'une équation cartésienne du plan est gx+hy+iz+j=0.
    #Pour trouver d, on cherche un point A du plan et on remplace x, y et z par les coordonnées de A.
    #equation plan perpendiculaire a (cd) passant par d
    
    dc = [(1/(d[0]-c[0]), -c[0]/(d[0]-c[0])), (1/(d[1]-c[1]), -c[1]/(d[1]-c[1])), (1/(d[2]-c[2]), -c[2]/(d[2]-c[2]))]
    ac = [(1/(a[0]-c[0]), -c[0]/(a[0]-c[0])), (1/(a[1]-c[1]), -c[1]/(a[1]-c[1])), (1/(a[2]-c[2]), -c[2]/(a[2]-c[2]))]
    #equation (ac)
    
    z=(-((ac[2][1]*g-ac[0][1]*g)/ac[0][0])-((ac[2][1]*h-ac[1][1]*h)/ac[1][0])-j)/(((ac[2][0]*g)/(ac[0][0]))+((ac[2][0]*h)/(ac[1][0]))+i)
    print(z)
    p1 = ac[2][0]*z + ac[2][1] - ac[0][1]
    x = p1/ac[0][0]
    y = (x*ac[0][0]+ac[0][1]-ac[1][1])/ac[1][0]
    b = (x,y,z)

    foc=0.0001
    m = (d[0]+foc,d[1]+foc,d[2])
    

    z_k = d[2]
    
    #sqrt((d[0]-b[0])**2 + (d[1]-b[1])**2 + (d[2]-b[2])**2) -x_k**2 -y_k**2 -d[2]**2 = 0
    #gx_k+hy_k+id[2]+j=0

    #   g*x_k+h*y_k+i*d[2]+j = sqrt((d[0]-b[0])**2 + (d[1]-b[1])**2 + (d[2]-b[2])**2) -x_k**2 -y_k**2 -d[2]**2
    #

    #     g*x_k+h*y_k+i*d[2]+j = b[0]*d[0]-b[1]*d[1]+Kx²+Ky²-Kx(d[0]+b[0])-Ky(d[1]+b[1])
    #     b[0]*d[0]-b[1]*d[1]+Kx²+Ky²-Kx(d[0]+b[0])-Ky(d[1]+b[1]) - g*Kx - h*Ky - i*d[2] - j = 0
    #     b[0]*d[0]-b[1]*d[1]+Kx²+Ky²-Kx(d[0]+b[0])-Ky(d[1]+b[1]) - g*Kx - i*d[2] - j = h*Ky
    #     b[0]*d[0]/h-b[1]*d[1]/h+Kx²/h+Ky²/h-Kx(d[0]+b[0])/h-Ky(d[1]+b[1])/h - g*Kx/h - i*d[2]/h - j/h = Ky
    #     b[0]*d[0]/h-b[1]*d[1]/h+Kx²/h+Ky²/h-Kx(d[0]+b[0])/h-g*Kx/h - i*d[2]/h - j/h = Ky(1+(d[1]+b[1])/h)
    #     b[0]*d[0]/h/(1+(d[1]+b[1])/h)-b[1]*d[1]/h/(1+(d[1]+b[1])/h)+Kx²/h/(1+(d[1]+b[1])/h)+Ky²/h/(1+(d[1]+b[1])/h)-Kx(d[0]+b[0])/h/(1+(d[1]+b[1])/h)-g*Kx/h/(1+(d[1]+b[1])/h) - i*d[2]/h - j/h = Ky
    #     b[0]*d[0]/h/(1+(d[1]+b[1])/h)-b[1]*d[1]/h/(1+(d[1]+b[1])/h)+Kx²/h/(1+(d[1]+b[1])/h)-Kx(d[0]+b[0])/h/(1+(d[1]+b[1])/h)-g*Kx/h/(1+(d[1]+b[1])/h) - i*d[2]/h - j/h - 1/(-b[1]-d[1]-h) = Ky
    #
    #     g*Kx*(1+d[1]/h+b[1]/h) +   Kx(Kx-(d[0]+b[0])-g)   =    (-j-i*d[2] +j+i*d[2]+ 1/(-b[1]-d[1]-h)  +  b[1]*d[1]/(1+(d[1]+b[1])/h) -   b[0]*d[0]/(1+(d[1]+b[1])/h))*(1+(d[1]+b[1])/h)
    #     Kx(g*h+d[1]*g+b[1]*g)/h   +   Kx(Kx-(d[0]+b[0])-g)  = 
    #     (g + d[1]*g/h + b[1]*g/h   +   Kx-d[0]-b[0]-g) /Kx =
    #     1 + g/Kx + d[1]*g/h/Kx + b[1]*g/h/Kx   +   d[0]/Kx-b[0]/Kx-g/Kx =
    #     (g + d[1]*g/h + b[1]*g/h + d[0]-b[0]-g)* 1/Kx = (-j-i*d[2] +j+i*d[2]+ 1/(-b[1]-d[1]-h)  +  b[1]*d[1]/(1+(d[1]+b[1])/h) -   b[0]*d[0]/(1+(d[1]+b[1])/h))*(1+(d[1]+b[1])/h)  -1
    x_k = ((g + d[1]*g/h + b[1]*g/h + d[0]-b[0]-g))  /  ((-j-i*d[2] +j+i*d[2]+ 1/(-b[1]-d[1]-h)  +  b[1]*d[1]/(1+(d[1]+b[1])/h) -   b[0]*d[0]/(1+(d[1]+b[1])/h))*(1+(d[1]+b[1])/h)  -1)

    y_k = (-j-i*z_k-g*x_k)/h

    
    k = (x_k,y_k,z_k)



    print(f"d {d} k {k}, b {b}")
    

    db = vecteur(d,b)
    #distance((x1,y1,d[0]),d) distance reel entre le centre et l'x du point a , distance((x1,y1,d[0]),(x,y,z)) distance reel entre l'x,d[1] et le x,y du point a
    
    #print(distance(d,m))
    #print(b)
    #print(k, d)
    y_final= distance(k,b) if db[2]<0 else -distance(k,b)
    x_final = -distance(k,d) if distance(d,k)>distance(m,k) else distance(k,d)
    print(x_final,y_final)
    return (x_final,y_final)
    #point sur la cv

pos_on_screen()


"""
a_ = (relative_pos(A))

screen = (1920,1080)
print(a_*scall)
"""