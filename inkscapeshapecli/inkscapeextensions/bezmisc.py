'''
Copyright (C) 2010 Nick Drobchenko, nick@cnc-club.ru
Copyright (C) 2005 Aaron Spike, aaron@ekips.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''


def tpoint(xxx_todo_changeme7, xxx_todo_changeme8,t):
    (x1,y1) = xxx_todo_changeme7
    (x2,y2) = xxx_todo_changeme8
    return x1+t*(x2-x1),y1+t*(y2-y1)
def beziersplitatt(xxx_todo_changeme9,t):
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = xxx_todo_changeme9
    m1=tpoint((bx0,by0),(bx1,by1),t)
    m2=tpoint((bx1,by1),(bx2,by2),t)
    m3=tpoint((bx2,by2),(bx3,by3),t)
    m4=tpoint(m1,m2,t)
    m5=tpoint(m2,m3,t)
    m=tpoint(m4,m5,t)

    return ((bx0,by0),m1,m4,m),(m,m5,m3,(bx3,by3))
