function f(x)
implicit none
integer,parameter::dp=selected_real_kind(15)
integer::flagg,interval,i
real(dp),dimension(2)::y
real(dp)::h,itime,ftime,stepsize,ten,fifty
real(dp),intent(in)::x
real(dp)::f
interface
subroutine RKF(tstart,tend,y,dy,h,hmin,hmax,eps1,eps2,exitflag,n)
implicit none
integer,parameter::dp=selected_real_kind(15)
integer,intent(in)::n!#eqns
integer,intent(out)::exitflag
real(dp),intent(in)::Tstart,Tend,eps1,eps2,Hmin,Hmax
real(dp),dimension(:),intent(in)::y
real(dp)::T,Emax
!real(dp),dimension(n)::c1=2825/27648,c2=18575/48384,c3=13525/55296,c4=277/14336,c5=0.25,y4,ysave
real(dp),intent(inout)::h
interface
  function dy(t,y,n)
    integer,parameter::dp=selected_real_kind(15)
    integer,intent(in)::N
    real(dp),intent(in)::T
    real(dp),dimension(:)::y
    real(dp),dimension(n)::dy
   endfunction dy
 end interface
endsubroutine
  function dy(t,y,n)
    integer,parameter::dp=selected_real_kind(15)
    integer,intent(in)::N
    real(dp),intent(in)::T
    real(dp),dimension(:)::y
    real(dp),dimension(n)::dy
   endfunction dy
end interface

! Initial Rainbow Trout popultion is 4
y(1)=4

! Initial Brown Trout population is variable
y(2)=x

! Find the difference in population after 10 and 50 years
h=0.005
call RkF(0.0_dp,10.0_dp,y,dy,h,.000000001d0,100d0,0.000000001d0,0.01d0,flagg,2)
ten=y(1)
call RkF(10.0_dp,50.0_dp,y,dy,h,.000000001d0,100d0,0.000000001d0,0.01d0,flagg,2)
fifty=y(1)
f=fifty-ten
endfunction
