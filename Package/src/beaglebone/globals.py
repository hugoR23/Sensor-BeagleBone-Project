'''
@Author: Hugo Robellaz
All the global variables are stored here.
'''

DATABASE_FILENAME='dataSaved.csv'

TEMP={'id':'temp',
      'color': '#F58559',
      'plotColor': '#F14D0E',
      'title': 'Temperature',
      'unit': u"\u00b0"+"C"}

PRES={'id':'pres',
      'color': '#996633',
      'plotColor': '#996633',
      'title': 'Pressure',
      'unit': " hPa"}

HUMI={'id':'humi',
      'color': '#67BF74',
      'plotColor': '#67BF74',
      'title': 'Humidity',
      'unit': '%'}

LUMI={'id':'lumi',
      'color': '#FFCC33',
      'plotColor': '#FFCC33',
      'title': 'Luminance',
      'unit': " lux"}

SENSORTYPE={'temp':TEMP,
            'pres':PRES,
            'lumi':LUMI,
            'humi':HUMI}
