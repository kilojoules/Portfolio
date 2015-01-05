! This is a high-order Runge-Kutta numerical differential equation solver.
! This method uses a dynamically controlled step size, which 
! increases this algorithm's efficiency.
subroutine RKF(tstart,tend,y,dy,h,hmin,hmax,eps1,eps2,exitflag,n)
implicit none
integer,parameter::dp=selected_real_kind(15)
integer,intent(in)::n!#eqns
integer,intent(out)::exitflag
real(dp),intent(in)::Tstart,Tend,eps1,eps2,Hmin,Hmax
real(dp),dimension(:),intent(inout)::y
real(dp)::T,Emax
real(dp)::c1=2825/27648,c2=18575/48384,c3=13525/55296,c=277/14336,c5=0.25
real(dp),dimension(n)::y4,ysave
real(dp),intent(inout)::h
logical::short=.false.
real(dp),dimension(n)::k1,k2,k3,k4,k5,k6!insert k values please
integer::i
interface
  function dy(t,y,n)
  integer,parameter::dp=selected_real_kind(15)
  integer,intent(in)::N
  real(dp),intent(in)::T
  real(dp),dimension(:)::y
  real(dp),dimension(n)::dy
  endfunction dy
endinterface
T=Tstart
Do
  Ysave=Y(:n)
  k1=dy(t,y(:n),n)
  k2=dy(t+0.2*h,y(:)+0.2*k1*h,n)
  k3=dy(t+3*h/10,y(:n)+3*k1*h/40+9*k2*h/40,n)
  k4=dy(t+3*h/5,y(:n)+3*k1*h/10-9*k2*h/10+6*k3*h/5,n)
  k5=dy(t+h,y(:n)-11*k1*h/54+5*k2*h/2-70*k3*h/27+35*k4*h/27,n)
  k6=dy(t+7*h/8,y(:n)+1631*k1*h/55296+175*k2*h/512+575*k3*h/13824+44275*k4*h/110592+253*k5*h/4096,n)
  y4=y+(37*k1/378+250*k3/621+125*k4/594+512*k6/1771)*h
  y=y+(2825*k1/27648+18575*k3/48384+13525*k4/55296+277*k5/14336+0.25*k6)*h
  emax=maxval(abs((y(:n)-y4)/y(:n)))
  if(EMAX>Eps2)Then  !error is too big
    if(h<=hmin)then
      exitflag=-1 
      return
    endif
    h=h/2
    if(h<hmin)h=hmin
    y(:n)=ysave
  else !y is ok, move on
    t=t+h
  endif
  if(abs(t-tend)<1d-5)then
    exitflag=5
    return !done
  endif
  if(emax<eps1 .and.h<hmax)then
    h=h*2
    if(h>hmax)h=hmax
  endif
  if(t+h>tend)then  !next step is too long
    h=tend-t
  endif
enddo
end subroutine
