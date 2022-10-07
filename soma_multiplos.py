def soma(num):
    num -= 1
    multi_tres = num//3
    multi_cinco = num//5
    
    total = 0
    for i in range(multi_tres):
        total = total + (i + 1) * 3
        
    for i in range(multi_cinco):
        total = total + (i + 1) * 5
        
    return total
