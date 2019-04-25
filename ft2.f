      program main
      IMPLICIT REAL*8(A-H,O-Y),COMPLEX*16(Z)
      CHARACTER FLIN*40

      !parameter( dt = 0.02d0, ntime = 5000 )
      parameter( FLIN =  'new_current.dat'    )

      real(8), allocatable :: atauprobe(:),totj(:),totj0(:),time(:)

C-- Setting of probe pulse
      ns = 36
      dt = 0.02d0
      ntime = 2001     ! データの行数
      tau0probe=1.d0
      taudprobe=0.02d0
      wprobe=10.d0
      a0probe=0.001d0

      PI=4.D0*DATAN(1.D0)
      itprobeon=0
      itprobeoff=ntime-1
      allocate(atauprobe(0:ntime-1))
      allocate(time(itprobeon:ntime-1))
      allocate(totj0(itprobeon:ntime-1))
      allocate(totj(itprobeon:ntime-1))

      ! プローブ光
      do it=0,ntime-1
        tau=it*dt
        atauprobe(it)=apulse(tau,a0probe,tau0probe,taudprobe,wprobe)  !A_0,probe(t) (与える電場)を生成
      end do

      ! ファイル読み込み
      open(2,FILE=FLIN,FORM='FORMATTED',STATUS='OLD')
        do it=itprobeon,itprobeoff
          read(2,*) time(it),totj(it)
        end do
      close(2)
      do it = itprobeon,itprobeoff
        write(6,*) time(it),totj(it)
      end do
      !ntime = itprobeoff - itprobeon + 1
      !dt = time(2) - time(1)
      write(6,*) "same?:",ntime,itprobeoff-itprobeon
      write(6,*) "same?:",dt,time(2)-time(1)


      open(15,FILE="spectrum.txt",FORM='FORMATTED') !STATUSの指定がない時はunknown(処理系依存)
      write(6,2100)
      write(15,2100)
 2100 format(/1x,'  omega ','  Re A(w) ','   Im A(w) ','   Re J(w) ',
     *           '   Im J(w)  ','    Re Sigma(w)','  Im Sigma(w)')

      itajon=itprobeon;itajoff=itprobeoff
      ! itprobeon = 0
      ! itprobeoff = 5000 カレントの時間発展の計算の期間

ccc      nw=600
      nw=int(2.d0*pi/dt) != 2π/dt

      do iw=1,nw !なぜnwを使うか
        w0=2.d0*pi*(iw-1)/ntime
        w=w0/dt
        br=0.1d0   ! = η(元はbr=1.d0/ns)
        zw=cmplx(w,br)  ! = w + iη

C-- Simpson's rule
        zon=exp(cmplx(-br*itajon*dt,w*itajon*dt)) !   =exp[i(w+iη)t_0(またはt_min)]
        zoff=exp(cmplx(-br*itajoff*dt,w*itajoff*dt)) !=exp[i(w+iη)t_max]

        zat=atauprobe(itajon)*zon+atauprobe(itajoff)*zoff !積分の最初と最後の項を先に計算
         != A(t_0)exp[i(w+iη)t_0] + A(t_max)exp[i(w+iη)t_max]
         !A(t)のフーリエ変換に使用
        zj=totj(itajon)*zon+totj(itajoff)*zoff
         != j(t_0)exp[i(w+iη)t_0] + j(t_max)exp[i(w+iη)t_max] !積分の最初と最後の項を先に計算
         !カレントのフーリエ変換に使用

        do it=itajon+1,itajoff-1,2 !奇数部分の計算
          tau=it*dt
        zat=zat+4.d0*atauprobe(it)*exp(cmplx(-br*tau,w*tau)) !atauprobe(it) = A_0,probe(t) (与える電場) , 積分を行う文
        zj=zj+4.d0*totj(it)*exp(cmplx(-br*tau,w*tau))
        end do

        do it=itajon+2,itajoff-2,2 !偶数部分の計算
          tau=it*dt
        zat=zat+2.d0*atauprobe(it)*exp(cmplx(-br*tau,w*tau)) !上で計算してない部分の計算
        zj=zj+2.d0*totj(it)*exp(cmplx(-br*tau,w*tau)) 
        end do

        zat=zat*dt/3.d0 !=A(w)
        zj=zj*dt/3.d0   !=j(w)

        z=zj/zw/zat/cmplx(0.d0,1.d0)/ns
         !=j(w) / [i(w+iη)A(w)L]
        write(6,2200) w,zat,zj,z
        write(15,2200) w,zat,zj,z
      end do
 2200 format(1x,f8.4,2f12.6,2x,2f12.6,2x,2f12.6)


      CLOSE(15)
      STOP
      END

      function apulse(tau,a0,tau0,taud,w)
      IMPLICIT REAL*8(A-H,O-Y),COMPLEX*16(Z)
      apulse=a0*exp(-(tau-tau0)**2.d0/2.d0/taud**2.d0)*cos(w*(tau-tau0))
      end function
