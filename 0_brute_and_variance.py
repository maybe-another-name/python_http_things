from random import randint
from time import sleep

'''Numerical String formatting, ranges, and random sleeps'''
for le_brut in range(1001):
  sleepy_time = randint(300,2000)/1000
  print(f"sleeping for {sleepy_time}")
  sleep(sleepy_time)
  print(f"{le_brut:04}")
