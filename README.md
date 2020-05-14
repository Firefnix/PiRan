# PiRan: Random numbers

## 1. License
GNU LESSER GENERAL PUBLIC LICENSE
    Version 3, 29 June 2007

Copyright (C)  2007 Free Software Foundation, Inc. <https://fsf.org/>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA, or see
<https://www.gnu.org/licenses/>.

## 2. Project overview
  -  Author: Firefnix
  -  Coded in Python 3.8
  -  Licensed under LGPL-3-or-later
  -  Source code: [here][src]

# 3. Usage examples
To build the digits calculator and compute:
```py
from piran import build, compute
build() # pi.c -> pi.so
compute(1E6) # One million digits!
```
Note that this is only needed once.
Now we can really use the library:
```py
from piran import Random
r = Random() # Creates a cursor file
for i in range(10):
    print("unsigned int:", r.uint(10), "\nsigned int:", r.sint(-10, 10))

r.close() # Deletes the cursor file
```

[src]: https://github.com/Firefnix/PiRan
