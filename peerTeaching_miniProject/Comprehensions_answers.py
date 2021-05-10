--- list comprehension ---
lc_numbers_odd = [i for i in range(1, 25) if i%2 != 0]

print (lc_numbers_even)


--- dictionary comprehension ---
dc_cubes_even = {n : n**3 for n in range(1,16) if n %2 ==0}

print(dc_cubes_even)
