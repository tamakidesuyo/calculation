#coding:utf-8
import math
#import os
import re

t_inc = float(input("time increments: "))
t_num = int(input("number of points on time: "))

'''
Lx = int(input("Lx = "))
Ly = int(input("Ly = "))
a_0x = float(input("A_0x = "))
a_0y = float(input("A_0y = "))
t_0 = float(input("t_0 = "))
t_d = float(input("t_d = "))
w_p = float(input("ω_p = "))
phase = float(input("phase = "))
'''
Lx = 4
Ly = 4
t_hx = 1.0
t_hy = 1.0  
a_0x = 0.001
a_0y = 0.0
t_0 = 1.0
t_d = 0.02
w_p = 10.0
U = 10
#phase = math.pi/2.0  #x方向とy方向の位相差
phase = 0.0

periodic_x = False
periodic_y = True

f_sna = open('scenario.txt', 'w')

for j in range(t_num):
    i = j + 1
    time = t_inc*i - t_0
    #gauss = math.exp(-(time/(2.*t_d))**2)
    gauss = math.exp(-((time * time) / (2. * t_d * t_d))) 
    wave_x = math.cos(w_p*time)
    wave_y = math.cos(w_p*time + phase)
    potential_x = a_0x * gauss * wave_x
    potential_y = a_0y * gauss * wave_y
    re_peierls_x = math.cos(potential_x)
    re_peierls_y = math.cos(potential_y)
    im_peierls_x = math.sin(potential_x)
    im_peierls_y = math.sin(potential_y)

    print(round(t_inc*i,8), round(potential_x,8), round(potential_y,8))

    dir_name = 'PRESET/' #directory of output data
#    os.makedirs(dir_name, exist_ok=True)

    fname = dir_name + 'preset' + str(i) + '.dat' #output file name
    s_sna = 'Q:' + str(round(t_inc,5)) + ':' + str(round(t_inc,5)) + ':ns=1,preset=' + 'preset' + str(i) + '.dat'
    f_sna.write(s_sna + '\n')

   # f_in = open('preset.txt', 'r')
    f_out = open(fname, 'w')

    # chain
    for i in range(1,(Lx*Ly)):
        if i%Ly == 0: # t_x
            f_out.write(str(i) + ' ' + str(i+1) + ' (' + str(t_hx*re_peierls_x) + ',' + str(t_hx*im_peierls_x) + ')\n')
        else:        # t_y
            f_out.write(str(i) + ' ' + str(i+1) + ' (' + str(t_hy*re_peierls_y) + ',' + str(t_hy*im_peierls_y) + ')\n')
            
    # long range
    for i in range(1,(Lx*Ly)):
        if 0 < i%(2*Ly) < Ly:
            n = i%(2*Ly)
            j = -n + 2*Ly + 1 + (i//(2*Ly))*2*Ly
            if j <= Lx*Ly:
                f_out.write(str(i) + ' ' + str(j) + ' (' + str(t_hx*re_peierls_x) + ',' + str(t_hx*im_peierls_x) + ')\n')
    for i in range(1,(Lx*Ly)):
        if Ly < i%(2*Ly):
            n = i%Ly
            j = -n + 3*Ly + 1 + ((i//Ly)-1)*Ly
            if j <= Lx*Ly:
                f_out.write(str(i) + ' ' + str(j) + ' (' + str(t_hx*re_peierls_x) + ',' + str(t_hx*im_peierls_x) + ')\n')

    # periodic x
    if periodic_x == True:
        for i in range(1,(Lx*Ly)):
            if i <= Ly:
                if Lx%2 == 0:
                    f_out.write(str(i) + ' ' + str(Lx*Ly-i+1) + ' (' + str(t_hx*re_peierls_x) + ',' + str(t_hx*im_peierls_x) + ')\n')
                else:
                    f_out.write(str(i) + ' ' + str(2*Ly+i) + ' (' + str(t_hx*re_peierls_x) + ',' + str(t_hx*im_peierls_x) + ')\n')
    # periodic y
    if periodic_y == True:
        for i in range(Lx):
            f_out.write(str(i*Ly+1) + ' ' + str((i+1)*Ly) + ' (' + str(t_hy*re_peierls_y) + ',' + str(t_hy*im_peierls_y) + ')\n')

    # on-site Coulomb interaction U
    if U > 0:
        f_out.write('#U=' + str(round(U,6)))

    '''
    for line in f_in:
        if re.search('#', line): #Coulomb interaction terms in 'preset.txt'
            f_out.write(line)
        else:
            l = line.split()
            f_out.write(l[0] + ' ' + l[1] + ' (' + str(float(l[2])*re_peierls_x) +
                                            ',' + str(float(l[2])*im_peierls_x) + ')\n')

    f_in.close()
    '''
    f_out.close()

f_in = open('PRESET/preset1.dat', 'r') 
f2_out = open('preset.txt', 'w') 
for line in f_in:
    if re.search('#', line): #Coulomb interaction terms in 'preset.txt'
        f2_out.write(line)
    else:
        l = line.split()
        f2_out.write(l[0] + ' ' + l[1] + ' (' + str(1.0) + ',' + str(0.0) + ')\n')

f_in.close()
f2_out.close()

f_sna.close()
