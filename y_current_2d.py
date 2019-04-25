# coding: UTF-8
import math
import re

t_inc = float(input("time increments: "))
t_num = int(input("number of points on time: "))
fsweep = int(input("number of sweep for ground state: "))
Lx = int(input("Lx = "))
Ly = int(input("Ly = "))

#f_out = open('new_current.dat', 'w')
#f_out.write(str(0.0) + ' ' + str(0.0) + '\n')
#f_out.close()
f_out = open('new_current.dat', 'w')

for j in range(0,t_num+1):
    if j == 0:
        preset = 'preset.txt'
    else:                
        preset = 'PRESET/preset' + str(j) + '.dat'
    phys1 = 'OUTPUT/1_' + str(j+fsweep) + '_1.dat'
    phys2 = 'OUTPUT/2_' + str(j+fsweep) + '_1.dat'
    phys3 = 'OUTPUT/3_' + str(j+fsweep) + '_1.dat'
    phys4 = 'OUTPUT/4_' + str(j+fsweep) + '_1.dat' #sweepが終わった後のdataを参照

    f_preset = open(preset, 'r')
    f_phys1 = open(phys1, 'r')
    f_phys2 = open(phys2, 'r')
    f_phys3 = open(phys3, 'r')
    f_phys4 = open(phys4, 'r')

    d_preset = []
    k = 1
    for i in f_preset:
        if re.search('#',i):
            pass 
        elif k%Ly != 0 and k < Lx*Ly:
            d_preset += [i.split()]
        elif k > (Lx-1)*Ly + (Ly-1)*Lx + Ly:
            d_preset +=[i.split()]
        else:
            pass
        k += 1
    print(d_preset)
    for i in range(len(d_preset)):
        if int(d_preset[i][0]) <= int(d_preset[i][1]):
            d_preset[i] = d_preset[i][2].lstrip('\(').rstrip('\)').split(',')
            d_preset[i] = [float(d_preset[i][0]), -float(d_preset[i][1])] #なぜ虚部に−をつける？
        else:
            d_preset[i] = d_preset[i][2].lstrip('\(').rstrip('\)').split(',')
            d_preset[i] = [-float(d_preset[i][0]), -float(d_preset[i][1])]

    d_phys1 = []
    k = 1
    for i in f_phys1:
        if re.search('#',i):
            pass 
        elif k%Ly != 0 and k < Lx*Ly:
            d_phys1 += [i.split()]
        elif k > (Lx-1)*Ly + (Ly-1)*Lx + Ly:
            d_phys1 +=[i.split()]
        else:
            pass
        k += 1

    d_phys2 = []
    k = 1
    for i in f_phys2:
        if re.search('#',i):
            pass 
        elif k%Ly != 0 and k < Lx*Ly:
            d_phys2 += [i.split()]
        elif k > (Lx-1)*Ly + (Ly-1)*Lx + Ly:
            d_phys2 +=[i.split()]
        else:
            pass
        k += 1

    d_phys3 = []
    k = 1
    for i in f_phys3:
        if re.search('#',i):
            pass 
        elif k%Ly != 0 and k < Lx*Ly:
            d_phys3 += [i.split()]
        elif k > (Lx-1)*Ly + (Ly-1)*Lx + Ly:
            d_phys3 +=[i.split()]
        else:
            pass
        k += 1

    d_phys4 = []
    k = 1
    for i in f_phys4:
        if re.search('#',i):
            pass 
        elif k%Ly != 0 and k < Lx*Ly:
            d_phys4 += [i.split()]
        elif k > (Lx-1)*Ly + (Ly-1)*Lx + Ly:
            d_phys4 +=[i.split()]
        else:
            pass
        k += 1

    total = 0.0
    for i in range(len(d_preset)):
        d_phys = float(d_phys1[i][2]) * d_preset[i][1] + float(d_phys1[i][3]) * d_preset[i][0]
        d_phys += float(d_phys2[i][2]) * d_preset[i][1] - float(d_phys2[i][3]) * d_preset[i][0]
        d_phys += float(d_phys3[i][2]) * d_preset[i][1] + float(d_phys3[i][3]) * d_preset[i][0]
        d_phys += float(d_phys4[i][2]) * d_preset[i][1] - float(d_phys4[i][3]) * d_preset[i][0]
        total += d_phys
#phys2とphys4は第一項にも−がつきそうである

    #print(round(t_inc * j, 8), round(total,8))
    f_out.write(str(round(t_inc * j, 8)) + ' ' + str(round(total,8)) + '\n')

    f_preset.close()
    f_phys1.close()
    f_phys2.close()
    f_phys3.close()
    f_phys4.close()

f_out.close()
