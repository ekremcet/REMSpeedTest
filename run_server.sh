#!/bin/sh
python3 Server.py 33333 P &
bg
python3 Server.py 33334 D &
bg
python3 Server.py 33335 U &
bg

