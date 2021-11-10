import numpy as np

def IMC(peso, estatura):
    return peso/(estatura*estatura)

def evaluarIMC(imc):
    evaluacion=""
    if imc<18.5:
        evaluacion="Insuficiencia ponderal"
    if imc>=18.5 and imc<=24.9:
        evaluacion="Intervalo normal"
    if imc>=25:
        evaluacion="Sobrepeso"
    if imc>=30 and imc<35:
        evaluacion="Obesidad de clase 1"
    if imc>=35 and imc<40:
        evaluacion="Obesidad de clase 2"
    if imc>=40:
        evaluacion="Obesidad de clase 3"
    return evaluacion

def porcentajeGrasa(sexo, cintura, cuello, altura, caderas):
    if sexo=="Femenino":
        PG=495/((1.29579-0.35004*(np.log10(cintura+caderas-cuello))+0.22100*(np.log10(altura)))-450)
    else:
        PG=495/(1.0324-0.19077*(np.log10(cintura-cuello))+0.15456*(np.log10(altura)))-450
    return PG