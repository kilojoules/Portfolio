function dy(t,y,n)
implicit none
integer,parameter::dp=selected_real_kind(15)
integer,intent(in)::n
real(dp),intent(in)::t
real(dp),dimension(:)::y
real(dp),dimension(n)::dy

! Differential equations describing Brown and Rainbow Trout populations.
! 1st entry is Rainbow Trout and 2nd entry is Brown Trout
dy(1)=(1-0.007*y(1)-0.01*y(2))*y(1)
dy(2)=(0.75-0.007*y(1)-0.007*y(2))*y(2)
endfunction
