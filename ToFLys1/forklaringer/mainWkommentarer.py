from microbit import *
import time as t

VEML6030 = 0x10 #slave address, altså bare hva som er addressen til SDA (serial data) kabelen som kobles mellom microbiten og sensoren
ALS_CONF = 0x00 #konfigurasjonsaddressen til VEML (ALS stands for Ambient Light Sensor) hvor man endrer på gain og integration (fancy shutter speed)
#7 bit slave address = 0x10
#read address = 0x04
Config = 0b0 #brukes for å pushe konfigurasjoner gjennom 0x00(ALS_CONF)

ALS_GAIN = { #Alle de forskjellige gain-settingene som finnes (de er begrenset fordi kun er 2 bits avsatt til gain, og 2 bits kan kun ha 4 ulike stadier)
    "gain1" : 0b00,
    "gain2" : 0b01,
    "gain1/8" : 0b10,
    "gain1/4" : 0b11
}
ALS_IT = { #det samme som den over, bare for integration (fancy shutter speed). Vet ikke hvorfor det bare er 6 settinger når de kan ha 16, men det er manufacteren sin beslutning så idk
    "IT25" : 0b1100,
    "IT50" : 0b1000,
    "IT100" : 0b0000,
    "IT200" : 0b0001,
    "IT400" : 0b0010,
    "IT800" : 0b0011
}
ALS_GAIN_VALUE = { #de forskjellige verdiene for gain bare decimal. Brukes i raw-lux konversjon senere
    0b00: 1,
    0b01: 2,
    0b10: 0.125,
    0b11: 0.25
}
ALS_IT_MS = {
    0b1100: 25,
    0b1000: 50,
    0b0000: 100,
    0b0001: 200,
    0b0010: 400,
    0b0011: 800
}

A = button_a #microbit sine knapper. Forkorter de til A og B for QOL
B = button_b

class ConfigureSensor(): #konfigurer-sensor klassen. Sier seg selv
    def __init__(self, Gain, IT):
        self.Gain = Gain
        self.Integration = IT
    
    def AlterGain(self): 
        global Config
        Config = Config & ~(0b11 << 11) #okei. Denne logikken her er komplisert så jeg legger til forklaringen i en separat fil.
        Config = Config | (self.Gain << 11) #samma her

    def AlterIT(self):
        global Config
        Config = Config & ~(0b1111 << 6)
        Config = Config | (self.Integration << 6)


def RawToLux(Reading): #konverterer raw input til lux via en formel jeg absolutt ikke forstår (matematisk sett. Koden forstår jeg jo :)
    Resolution = (
        0.0042
        * (800 / ALS_IT_MS[Sensor.Integration])
        * (2 / ALS_GAIN_VALUE[Sensor.Gain])
    )
    Lux = Resolution * Reading
    Lux = (((6.0135e-13 * Lux - 9.3924e-9) * Lux + 8.1488e-5) * Lux + 1.0023) * Lux
    return Lux


try:
    Sensor = ConfigureSensor( #konfigurerer sensoren med pre-determined gain og it verdier. Ikke mulig å bruke f.eks input her fordi koden kjøres på microbiten
        ALS_GAIN["gain2"], #Bruker gain 2 fordi desto høyere gain, desto lettere er det å måle mørke verdier (kort fortalt)
        ALS_IT["IT200"] #200 IT er sånn versatile mengde som bør funke fint til mørkmåling
    )
except Exception as Error:
    print("an error occured:", Error)
    raise #om det kommer en feil i konfigureringen vil denne ta feilen og printe det ut
#egentlig hadde jeg denne fordi det var en input i sensor = configuresensor(xx) der, og det hadde da vært lettere for brukeren å se om de skrev noe feil, 
#men nå som jeg har fjerna inputen gidder jeg egentlig ikke fjerne denne, så den bare er der. Nyttig om det oppstår en feil ut av thin air, da (som ofte skjer, haha)
Sensor.AlterGain() #modifiserer config bitrekken
Sensor.AlterIT() #kan også se "de to config bytene" i stedet for bitrekken, da

i2c.init() #init står for initialize. Den initierer(starter) i^2c kommunikasjonen mellom microbiten og VEML.
i2c.write( 
    VEML6030, #i2c.write starter med å definere hvilken kanal kommunikasjonen skal skje på. Det er her variabelet fra starten (0x10) kommer in handy
    bytes([ALS_CONF, #dette er registeret inni sensoren som konfigureres. 0x00, som definert tidligere (det er ikke jeg som har definert, det er manufactureren)
        Config & 0xFF, #i2c kan kun frakte én byte (åtte bits) om gangen, så dette er de 8 første bitsene.
        (Config >> 8) & 0xFF #dette er de 8 siste bitsene
    ]))


while not A.is_pressed():
    t.sleep(1) #venter på at A blir trykket på microbiten før den begynner å logge data.


with open("data.txt", "a") as DataFile: #her åpner den 3 forskjellige filer som brukes til logging:
    with open("lux.txt", "a") as LuxFile: #Dataen som vi får direkte fra sensoren, lux-konvertert data og en for å måle hvor lang tid mellom hver måling
        with open("time_per_datapoint.txt", "a") as TimeFile:
            RunStartMS = running_time() #Håper denne sier seg selv. Det er når loggingen begynte (tiden mellom programmet startet og loggingen begynte).
            PreviousSampleMS = RunStartMS #Denne brukes til å måle tiden mellom hver måling

            while not (A.is_pressed() and B.is_pressed()): #tar målinger helt til A og B blir trykket samtidig. Da stopper den å logge/måle
                i2c.write(VEML6030, bytes([0x04]), repeat=True) #her sender vi til sensoren "0x04" og ingenting mer. Følger den opp med repeat = true. Dette gjør at det neste skjer i registeret 0x04, som er datalagringsregisteret
                Data = i2c.read(VEML6030, 2) #Her leser den og lagrer det som står i 0x04. Siden det er 16 bits nå det lagres i to bulker (to bytes. 8bits per byte vettu). [0] og [1]
                RawReading = Data[0] | (Data[1] << 8) #Her merge(kombinerer) programmet de to bytesene sammen til en, så den er lesbar.
                Lux = RawToLux(RawReading) #konverterer raw dataen til lux
                SampleTimeMS = running_time() #Viser når denne målingen tok slutt

                DataFile.write(str(RawReading) + "\n") #skriver i data-fila raw verdien, og lager en ny linje til neste verdi som gentlemanen den er :)
                LuxFile.write("{:.4f}\n".format(Lux)) #skriver lux dataen i spesiellformatteringen "lux(med 4 desimaler)" også en ny linje
                TimeFile.write(
                    str(SampleTimeMS - PreviousSampleMS) + "\n" #skriver hvor lang tid denne målingen tok
                )
                PreviousSampleMS = SampleTimeMS #forbereder til neste måling

                t.sleep_ms(200) #pause mellom hver måling. Siden integration time er 200, vil den ta 200ms å måle. Denne her forsikret at sensoren rekker å måle før den henter ut data neste gang

            RuntimeMS = running_time() - RunStartMS #total runtime etter all målingen er ferdig (a+b har blitt trykket :O)

with open("runtime.txt", "a") as RuntimeFile:
    RuntimeFile.write(str(RuntimeMS) + "\n") #skriver total runtime

Config = Config | 0b1 #her endrer den på den første biten i config. Det er power-biten ifølge konfigen til VEML6030
i2c.write(VEML6030, bytes([ALS_CONF,
    Config & 0xFF,
    (Config >> 8) & 0xFF])) #nå har den gitt bit 0 verdien 1. Det betyr "power off" :( RIP 
display.show(Image.HEART) #viser et hjerte på microbiten :) Så koselig!!!
t.sleep(1)