def fatorial(num):
    fat = 1
    if num >= 2:
        for i in range(num):
            fat = fat * (i + 1)
            
    return fat
