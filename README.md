# PiRan: Random numbers

## 1. License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## 2. Project overview
  -  Author: Firefnix
  -  Coded in Python 3.8
  -  Licensed under GPL-3-or-later
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

[src]: <will be added later>
