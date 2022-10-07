class Votos():
    def votos_validos(total = 1000, validos = 800):
        return "{:.0%}".format(validos / total)
    
    def votos_brancos(total = 1000, brancos = 150):
        return "{:.0%}".format(brancos / total)
    
    def votos_nulos(total = 1000, nulos = 50):
        return "{:.0%}".format(nulos / total)
    