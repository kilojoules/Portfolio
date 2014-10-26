! Julian Quick

! This program simulates a pond with populations of 
! Brown and Rainbow Trout.
! The shooting method is used to find an initial 
! population of Brown Trout (The dominant species)
! that will result in a stable popultion of rainbow trout.

! This is accomplished by supplying two initial guesses of the 
! Brown trout population, then solving for the difference in 
! rainbow trout population after 10 and 50 years.
! The secant numerical root-finding method was used to find
! an initial Brown Trout population such that the fluctuation in 
! rainbow trout population is minimized

! The Runge-Kutta numerical method is used to solve a system of two differential
! equations, using a dynamicly controlled step size
program runtutututa
implicit none
integer,parameter::dp=selected_real_kind(15)
real(dp)::x1,x2,Sout
interface
  subroutine secant(x1,x2,sout)
   implicit none
   integer,parameter::dp=selected_real_kind(15)
   real(dp),intent(in)::x1,x2
   real(dp),intent(out)::sout
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
   end interface
   endfunction
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

! Initial Brown Trout population estimates are 19 and 19.5 trout per square foot
call secant(19.0_dp,19.50_dp,Sout)
write(*,*)Sout
endprogram
