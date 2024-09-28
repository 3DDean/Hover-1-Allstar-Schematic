import re

# Pin Name	Pins 	Pin Type(1)	I/O Level(2)	Functions description
pinDefinitions = """
VBAT	1	P	Default: VBAT
PC13-TAMPER-RTC	2	I/O	Default: PC13	Additional : RTC_TAMP0, RTC_TS, RTC_OUT, WKUP1
PC14-OSC32IN	3	I/O	Default: PC14	Additional : OSC32IN
PC15-OSC32OUT	4	I/O	Default: PC15	Additional : OSC32OUT
PF0-OSCIN	5	I/O	5VT	Default: PF0	Additional : OSCIN
PF1-OSCOUT	6	I/O	5VT	Default: PF1	Additional : OSCOUT
NRST	7	I/O	Default: NRST
VSSA	8	P	Default: VSSA
VDDA	9	P	Default: VDDA
PA0-WKUP	10	I/O	Default: PA0	Alternate: USART0_CTS(3), USART1_CTS(4), TIMER1_CH0, TIMER1_ETI, I2C1_SCL(5)	Additional : ADC_IN0, RTC_TAMP1, WKUP0
PA1	11	I/O	Default: PA1	Alternate: USART0_RTS(3)/USART0_DE(3), USART1_RTS(4)/USART1_DE(4), TIMER1_CH1, I2C1_SDA(5), EVENTOUT	Additional : ADC_IN1
PA2	12	I/O	Default: PA2	Alternate: USART0_TX(3), USART1_TX(4), TIMER1_CH2, TIMER14_CH0	Additional : ADC_IN2
PA3	13	I/O	Default: PA3	Alternate: USART0_RX(3), USART1_RX(4), TIMER1_CH3, TIMER14_CH1	Additional : ADC_IN3
PA4	14	I/O	Default: PA4	Alternate: SPI0_NSS, USART0_CK(3), USART1_CK(4), TIMER13_CH0, SPI1_NSS(5)	Additional : ADC_IN4
PA5	15	I/O	Default: PA5	Alternate: SPI0_SCK, TIMER1_CH0, TIMER1_ETI	Additional : ADC_IN5
PA6	16	I/O	Default: PA6	Alternate: SPI0_MISO, TIMER2_CH0, TIMER0_BRKIN, TIMER15_CH0, EVENTOUT	Additional : ADC_IN6
PA7	17	I/O	Default: PA7	Alternate: SPI0_MOSI, TIMER2_CH1, TIMER13_CH0, TIMER0_CH0_ON, TIMER16_CH0, EVENTOUT	Additional : ADC_IN7
PB0	18	I/O	Default: PB0	Alternate: TIMER2_CH2, TIMER0_CH1_ON, USART1_RX(4), EVENTOUT	Additional : ADC_IN8
PB1	19	I/O	Default: PB1	Alternate: TIMER2_CH3, TIMER13_CH0, TIMER0_CH2_ON, SPI1_SCK(5)	Additional : ADC_IN9
PB2	20	I/O	5VT	Default: PB2
PB10	21	I/O	5VT	Default: PB10	Alternate: I2C1_SCL(5), TIMER1_CH2
PB11	22	I/O	5VT	Default: PB11	Alternate: I2C1_SDA(5), TIMER1_CH3, EVENTOUT
VSS	23	P	Default: VSS
VDD	24	P	Default: VDD
PB12	25	I/O	5VT	Default: PB12	Alternate: SPI0_NSS(3), SPI1_NSS(5), TIMER0_BRKIN, I2C1_SMBA(5), EVENTOUT
PB13	26	I/O	5VT	Default: PB13	Alternate: SPI0_SCK(3), SPI1_SCK(5), TIMER0_CH0_ON
PB14	27	I/O	5VT	Default: PB14	Alternate: SPI0_MISO(3), SPI1_MISO(5), TIMER0_CH1_ON, TIMER14_CH0
PB15	28	I/O	5VT	Default: PB15	Alternate: SPI0_MOSI(3), SPI1_MOSI(5), TIMER0_CH2_ON, TIMER14_CH0_ON, TIMER14_CH1	Additional : RTC_REFIN
PA8	29	I/O	5VT	Default: PA8	Alternate: USART0_CK, TIMER0_CH0, CK_OUT, USART1_TX(4), EVENTOUT
PA9	30	I/O	5VT	Default: PA9	Alternate: USART0_TX, TIMER0_CH1, TIMER14_BRKIN, I2C0_SCL
PA10	31	I/O	5VT	Default: PA10	Alternate: USART0_RX, TIMER0_CH2, TIMER16_BRKIN, I2C0_SDA
PA11	32	I/O	5VT	Default: PA11	Alternate: USART0_CTS, TIMER0_CH3, EVENTOUT
PA12	33	I/O	5VT	Default: PA12	Alternate: USART0_RTS/USART0_DE, TIMER0_ETI, EVENTOUT
PA13	34	I/O	5VT	Default: PA13	Alternate: IFRP_OUT, SWDIO, SPI1_MISO(5)
PF6	35	I/O	5VT	Default: PF6	Alternate: I2C1_SCL(5), I2C0_SCL(6)
PF7	36	I/O	5VT	Default: PF7	Alternate: I2C1_SDA(5), I2C0_SCL(6)
PA14	37	I/O	5VT	Default: PA14	Alternate: USART0_TX(3), USART1_TX(4), SWCLK, SPI1_MOSI(5)
PA15	38	I/O	5VT	Default: PA15	Alternate: SPI0_NSS, USART0_RX(3), USART1_RX(4), TIMER1_CH0, TIMER1_ETI, SPI1_NSS(5), EVENTOUT
PB3	39	I/O	5VT	Default: PB3	Alternate: SPI0_SCK, TIMER1_CH1, EVENTOUT
PB4	40	I/O	5VT	Default: PB4	Alternate: SPI0_MISO, TIMER2_CH0, EVENTOUT
PB5	41	I/O	5VT	Default: PB5	Alternate: SPI0_MOSI, I2C0_SMBA, TIMER15_BRKIN, TIMER2_CH1
PB6	42	I/O	5VT	Default: PB6	Alternate: I2C0_SCL, USART0_TX, TIMER15_CH0_ON
PB7	43	I/O	5VT	Default: PB7	Alternate: I2C0_SDA, USART0_RX, TIMER16_CH0_ON
BOOT0	44	I	Default: BOOT0
PB8	45	I/O	5VT	Default: PB8	Alternate: I2C0_SCL, TIMER15_CH0
PB9	46	I/O	5VT	Default: PB9	Alternate: I2C0_SDA, IFRP_OUT, TIMER16_CH0, EVENTOUT
VSS	47	P	Default: VSS
VDD	48	P	Default: VDD"""

pinTypeMapping = {"I/O" : "bidirectional", "P": "power_in", "I" : "input"}

f = open("pinDefs.txt", "w")

pinOutput = ""
yPos = 0

for match in re.findall(".+\n", pinDefinitions):
    pinFields = re.split("\t", match)
    defaultName = pinFields[0]
    pinNumber = pinFields[1]
    pinType = pinFields[2]
    ioLevel = pinFields[3]
    alternateFunction = []
    additionalFunction = []

    for remainingFields in pinFields[4:]:
        pinFunction = re.match("(Alternate|Additional|Default)\s*:\s*(.+)", remainingFields)
        if pinFunction[1] == "Default":
            defaultName = pinFunction[2]
        elif pinFunction[1] == "Alternate":
            alternateFunction = pinFunction[2].split(", ")
        elif pinFunction[1] == "Additional":
            additionalFunction = pinFunction[2].split(", ")
        else:
            raise "Formatting incorrect"

    # TODO replace with string stream
    pinDefinition = ""
    pinDefinition += "			(pin " + pinTypeMapping[pinType] + " line\n"
    pinDefinition += "				(at -2.54 " + str(yPos) + " 0)\n"
    
    pinDefinition += "				(length 2.54)\n"
    pinDefinition += "				(name \"" + defaultName + "\"\n"
    pinDefinition += "					(effects\n"
    pinDefinition += "						(font\n"
    pinDefinition += "							(size 1.27 1.27)\n"
    pinDefinition += "						)\n"
    pinDefinition += "					)\n"
    pinDefinition += "				)\n"
    pinDefinition += "				(number \""+ str(pinNumber) + "\"\n"
    pinDefinition += "					(effects\n"
    pinDefinition += "						(font\n"
    pinDefinition += "							(size 1.27 1.27)\n"
    pinDefinition += "						)\n"
    pinDefinition += "					)\n"
    pinDefinition += "				)\n"
    for name in alternateFunction:
        pinDefinition += "				(alternate \"" + name + "\" " + pinTypeMapping[pinType] + " line)\n"

    for name in additionalFunction:
        pinDefinition += "				(alternate \"" + name + "\" unspecified line)\n"

    pinDefinition += "			)\n"
    pinOutput += pinDefinition
    yPos -= 2.54

# print(pinOutput)

f = open("pinDefs.txt", "w")
f.write(pinOutput)
f.close()
