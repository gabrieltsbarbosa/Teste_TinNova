def bubble_sort(vet = [5, 3, 2, 4, 7, 1, 0, 6]):
    for i in range(len(vet) - 1):
        for j in range(len(vet) - (i + 1)):
            if vet[j] < vet[j + 1]:
                vet[j], vet[j + 1] = vet[j + 1], vet[j]
                
    return vet
