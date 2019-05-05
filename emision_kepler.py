import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


## CONFIGURACIÓN DE LA MONEDA ##

COIN = 100 * 1000 * 1000 #Considera 8 decimales

nSubsidyInicial = 14 * COIN #Cantidad inicial de monedas por bloque
nHeight = 0 # nro de bloque inicial
premine = 600000 * COIN # Preminado en el bloque nHeight = 1
blockTime = 2 # Tiempo de minado de cada bloque en minutos
genesisTime = 2322332 # Tiempo del bloque genesis en formato Unix Timestamp # NO IMPLEMENTADO AUN

debug = False # activar debugging si rompo algo (que si lo voy a hacer :D)

mill = 1000000
k = 1000

def GetBlockSubsidy(nHeight):
    global nSubsidyInicial
    nSubsidy = premine if nHeight == 1 else nSubsidyInicial
    #nSubsidy = 14 * COIN 
    if(nHeight < (43800/2) and nHeight != 1): # periodo de un mes para incentivar el minado
        nSubsidy = 50 * COIN
        return nSubsidy
    nSubsidy >>= (nHeight // 1051200) #4y in mins 2102400 con calc programador de windows, se pueden hacer hasta 31 rightshifts
    # nSubsidy = nSubsidy >> (nHeight // 210000)
    #nSubsidy >>= nHeight / 1000
    #al llegar al bloque X, se divide el reward en 2
    #if nHeight == 10000:
        #nSubsidy == nSubsidy/2
    return nSubsidy

def GetMNPayout(nSubsidy, nHeight):
    ret = 0 # 25% del block reward
    startMNPayments = 21900 #KPL 43800 mins 1 mes
    step = 10080/2 # cambia cada 5040 bloques # 1 semana 
    #startIncrease = startMNPayments + 1000 # los steps (pasos) empiezan desde este bloque

    if nHeight > startMNPayments:
        ret = nSubsidy * .25 # 25% del block reward
    if nHeight > startMNPayments + step:  # si la altura es mayor a 1000
         ret = nSubsidy * .30 # 30% del block reward
    if nHeight > startMNPayments + (step * 2): # step 2, bloque 1000 + step
         ret = nSubsidy * .35 # 35%
    if nHeight > startMNPayments + (step * 3):  
         ret = nSubsidy * .40
    return ret

def main():

    global nSubsidyInicial, nHeight 
    nSubsidy = nSubsidyInicial
    nHeight = nHeight

    mill = 1000000
    k = 1000

    total = 0
    totalMN = 0

    dataYears = []
    dataGen = []
    dataMN = []

    while nSubsidy != 0:

        nSubsidy = GetBlockSubsidy(nHeight) 
        mnPayout = GetMNPayout(nSubsidy, nHeight)
        if (nSubsidy/10**8 < 0.001): # asi termina mas rapido el loop y no hay errores raros 0.001
            print("Loop termino en bloque: " + str(nHeight-1) + " nSubsidy: " + str(GetBlockSubsidy(nHeight-1)/10**8) + " mnpay: "+ str(GetMNPayout(GetBlockSubsidy(nHeight-1), nHeight-1)/10**8) + " tiempo:" + str(blockTime*(nHeight-1)))
            break
        
        total += nSubsidy
        totalMN += mnPayout
        if not(nHeight % 10000) or (nHeight < 2): # solo obtener multiplos de 10000 como datos y bloque 0 y 1 por el premine
            dataYears.append((blockTime*nHeight)/60 /24 /365.25)
            dataGen.append(total/10**8/mill)
            dataMN.append(totalMN/10**8/mill)
        
        if (False) and not(nHeight % 1051200):
            print("block:", nHeight, "time", (blockTime*nHeight)/60 /24 /365.25 )

        if(debug):
            print("bloque: " + str(nHeight) + " nSubsidy: " + str(nSubsidy/10**8) + " mnpay: "+ str(mnPayout/10**8) + " tiempo:" + str(blockTime*nHeight))
        if (nHeight == 1):
            print (total / float(COIN))
        nHeight += 1

    
    print(total / float(COIN))
    print((blockTime*nHeight)/60 /24 /365.25 )

    def millions(y, pos):
        'The two args are the value and tick position'
        return (str(y) + "M")

    # kk
    formatter = FuncFormatter(millions)
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(formatter)

    plt.plot(dataYears, dataGen, dataYears, dataMN)
    plt.title('Gráfico de Emisión')
    plt.ylabel('Emision Kepler (en millones)')
    plt.xlabel('Años desde genesis')
    plt.show()


    #print("bloque: " + str(nHeight) + " nSubsidy: " + str(nSubsidy/10**8) + " mnpay: "+ str(ret/10**8) + " tiempo:" + str(10*nHeight))

    #print(total / float(COIN))*2


if __name__ == "__main__":
    main()