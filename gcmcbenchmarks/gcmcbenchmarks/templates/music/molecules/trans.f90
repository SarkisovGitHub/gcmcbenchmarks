character(len=1) :: name(500)
character(len=10) :: name1(500)
real :: x(500), y(500), z(500)

open(10, file = "IRMOF1.in", status = "unknown")
open(11, file = "IRMOF1.mol", status = "unknown")

read(*,*) XL
YL=XL
ZL=XL

read(10,*) nmol

do i=1, nmol

read(10,*) i4, x(i), y(i), z(i), name(i), a, a, a
end do


do i=1, nmol
if(name(i) == "Z") then
name1(i) = "Zinc"
charge = 1.333

elseif(name(i) == "C") then
name1(i) = "Carbon"
charge = 0.106

do j=1, nmol

if(j==i) cycle

dx=x(i) - x(j)
dx = dx - XL*real(int(2.0*dx/XL))
dy=y(i)	- y(j)
dy = dy	- YL*real(int(2.0*dy/YL))
dz=z(i)	- z(j)
dz = dz	- ZL*real(int(2.0*dz/ZL))

dist = dx*dx + dy*dy + dz * dz
dist = sqrt(dist)

if(name(j)=="O".and.dist<1.5) then
charge = 0.558
exit
elseif(name(j)=="H".and.dist<1.0) then
charge = -0.167
exit
end if

end do



elseif(name(i) == "O")	then
name1(i) = "Oxygen"
charge = -1.564

do j=1, nmol

if(j==i) cycle

dx=x(i) - x(j)
dx = dx - XL*real(int(2.0*dx/XL))
dy=y(i) - y(j)
dy = dy - YL*real(int(2.0*dy/YL))
dz=z(i) - z(j)
dz = dz - ZL*real(int(2.0*dz/ZL))

dist = dx*dx + dy*dy + dz * dz
dist = sqrt(dist)

if(name(j)=="C".and.dist<1.5) then
charge = -0.641
exit
end if

end do

elseif(name(i) == "H")	then
name1(i) =	"Hydrogen"
charge = 0.162
else
endif

print*, name1(i)
write(11,'(i4, 3F10.5, a, F10.5, a)') i, x(i), y(i), z(i), "    "//name1(i), charge, "  0    0"
write(20,*) name(i), x(i), y(i), z(i), charge

end do
end
