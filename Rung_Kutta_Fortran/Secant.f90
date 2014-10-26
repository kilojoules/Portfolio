! Secant Method is used to find the initial population of
! brown trout which will result in a stable population of
! rainbow trout
subroutine secant(x1,x2,secantout)
implicit none
interface
   function f(x)
   integer,parameter::dp=selected_real_kind(15)
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
   endinterface
   endfunction
endinterface
integer,parameter::dp=selected_real_kind(15)
integer::i
real(dp),intent(in)::x1,x2
real(dp)xnew,xcurr,xpast
real(dp),intent(out)::secantout
xcurr=x2
xpast=x1
i=1
do
  xnew=xcurr-f(xcurr)*(xcurr-xpast)/(f(xcurr)-f(xpast))
  if(abs(f(xcurr)-f(xnew))<0.00001)THEN
    exit
  endif
  xpast=xcurr
  xcurr=xnew
  i=i+1
write(*,*)xnew
enddo
secantout=xnew
endsubroutine
!================================================
