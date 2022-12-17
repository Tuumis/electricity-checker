'''
Script for changing the color of the WiZ-smart light
debendig of the price of electricity compared to day's average.
The controlling of the bulb is done with pywizlight library.
The current price and the day's average is taken from the page spottihinta.fi.

'''
from bs4 import BeautifulSoup
import re
import urllib.request
import time
import asyncio
from pywizlight import wizlight, PilotBuilder, discovery

async def main():
    #initialise the bulb with local ip-address of the bulb
    light = wizlight('192.168.1.84')
    
    #page where to read which is part of the request body
    url = 'https://spottihinta.fi'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    #looping forever to check price and update light correctly
    while(True):
        #fetching the page info and parsing the necessary data
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        now = soup.find_all('div', attrs = {'class' : 'price-current-color'})[-1].text
        average = soup.find_all('div', attrs = {'class' : 'price-current-color'})[1].text
        price = now.split()[3]
        avgprice = average.split()[1]
        
        #printing time, this moment price and day's average price
        print(time.ctime())
        print('Nyt:', price, 'snt/kwh')
        print('Keskiarvo:', avgprice, 'snt/kwh')
        
        '''
        Taking the first digits before desimal splitter for comparing.
        Comparing only the first digits might make mistakes
        when the actual values are close but lazines won.
        '''
        pri = int(price.split(',')[0])
        avg = int(avgprice.split(',')[0])
        
        '''
        Comparing the price to average and changing the color acordingly.
        Green if lower then average.
        Red if higher then average.
        Blue if about the same as the average.
        Colors can be changed by changing the rgb values
        and with adding elif's and comparing how much values differ
        would be possible to adjust color to light or dark version of the color.
        So dark red would be extremly high price compared to average
        and the light red would be close to average.
        '''
        if (avg < pri):
            print('that is pricy')
            await light.turn_on(PilotBuilder(rgb = (255, 0, 0)))
        elif(avg > pri):
            print('wow, it is cheap')
            await light.turn_on(PilotBuilder(rgb = (0, 255, 0)))
        else:
            print('well, it is okay')
            await light.turn_on(PilotBuilder(rgb = (0, 0, 255)))
            
        #sleeping 20 min before upgrading the price by multiplying 60 seconds by 20
        time.sleep(60*20)
    
if __name__=="__main__":
    asyncio.run(main())