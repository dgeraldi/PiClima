#!/usr/bin/python

#Reference: https://en.wikipedia.org/wiki/Heat_index#Formula


__title__ = 'PiClima - Heat Index'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'


class HeatIndex:
    """Heat Index Calculation"""

    def calcHeatIndex(self, temp_celsius, hum):

        #print(f"HI Temperature: {temp_celsius} Humidity: {hum}")

        # Constants for Celsius calculations
        c1 = -8.78469475556
        c2 = 1.61139411
        c3 = 2.33854883889
        c4 = -0.14611605
        c5 = -0.012308094
        c6 = -0.0164248277778
        c7 = 0.002211732
        c8 = 0.00072546
        c9 = -0.000003582

        # Calculate heat index in Celsius
        heat_index_celsius = (
            c1 +
            c2 * temp_celsius +
            c3 * hum +
            c4 * temp_celsius * hum +
            c5 * temp_celsius**2 +
            c6 * hum**2 +
            c7 * temp_celsius**2 * hum +
            c8 * temp_celsius * hum**2 +
            c9 * temp_celsius**2 * hum**2
        )

        return heat_index_celsius