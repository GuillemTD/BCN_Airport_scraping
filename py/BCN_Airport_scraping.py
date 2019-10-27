#!/usr/bin/env python
# coding: utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# initialisation of the columns
c_fdate = []
c_fdest = []
c_fdest_city = []
c_fdest_iata = []
c_fair = []
c_fnum = []
c_fhour = []
c_ftype = []
c_fterm = []
c_fstatus_all = []

# data is stored in 8 different links
page = ['https://www.barcelona-airport.com/eng/departures.php?tp=0&day=yesterday',
       'https://www.barcelona-airport.com/eng/departures.php?tp=6&day=yesterday',
       'https://www.barcelona-airport.com/eng/departures.php?tp=12&day=yesterday',
       'https://www.barcelona-airport.com/eng/departures.php?tp=18&day=yesterday',
       'https://www.barcelona-airport.com/eng/arrivals.php?tp=0&day=yesterday', 
        'https://www.barcelona-airport.com/eng/arrivals.php?tp=6&day=yesterday', 
        'https://www.barcelona-airport.com/eng/arrivals.php?tp=12&day=yesterday',
        'https://www.barcelona-airport.com/eng/arrivals.php?tp=18&day=yesterday']

# looping the 8 links
for link in page:
    html = urlopen(link)
    bs = BeautifulSoup(html.read(), 'html.parser')
    # obtaining the scheduled date of the flight and the destination/origin
    flights_date = bs.find('div', {'class': 'flights'})
    x1 = flights_date.get_text().split('\n')
    y2 = x1[1].split(': ')
    fdest = bs.find_all(id='fdest')
    i = 0
    for name in fdest:
        if i > 0:
            c_fdest.append(name.get_text())
            x = name.get_text().split('  (')
            c_fdest_city.append(x[0]) #name of the city's airport
            y = x[1].split(' ')
            c_fdest_iata.append('('+y[0]) #iata code of the airport
            c_fdate.append(y2[1])
        i = i+1
    # obtaining the airline name
    fair = bs.find_all(id='fair')
    i = 0
    for name in fair:
        if i > 0:
            c_fair.append(name.get_text())
        i = i+1

    # obtaining flight number
    fnum = bs.find_all(id='fnum')
    i = 0
    for name in fnum:
        if i > 0:
            c_fnum.append(name.get_text().replace(" ", ""))
        i = i+1

    # obtaining the scheduled time
    fhour = bs.find_all(id='fhour')
    i = 0
    for name in fhour:
        if i > 0:
            c_ftype.append(fhour[0].get_text())
            c_fhour.append(name.get_text())
        i = i+1

    # obtaining the terminal
    fterm = bs.find_all(id='fterm')
    i = 0
    for name in fterm :
        if i > 0:
            c_fterm.append(name.get_text())
        i = i+1

    # obtaining the status of the flight
    fstatus_all = bs.find_all(id=('fstatus', 'fstatus_G', 'fstatus_GR', 'fstatus_R', 'fstatus_Y', 'fstatus_O'))
    i = 0
    for name in fstatus_all:
        if i > 0:
            x = name.get_text().split(' [')
            c_fstatus_all.append(x[0])
        i = i+1


c_date_real = []
c_time_real = []
c_gate = []
link_dep_ini = 'https://www.barcelona-airport.com/eng/flight-departure/'
link_arr_ini = 'https://www.barcelona-airport.com/eng/flight-arrival/'
link_fi = '?day=yesterday'

i=0
# looping all the flight numbers
for fnr in c_fnum:
    # Option 1: Departure
    if c_ftype[i] == 'Departure':
        link_all = link_dep_ini + fnr + link_fi
        html = urlopen(link_all)
        bs = BeautifulSoup(html.read(), 'html.parser')
        f_real = bs.find(id='flight_dep')
        f_real_x = f_real.get_text().split('\n')
        c_time_real_x1 = f_real_x[4].split('(')
        if len(c_time_real_x1) == 1:
            c_time_real_x2 = f_real_x[4].split(':')
            c_time_real.append(c_time_real_x2[1].strip() + ':' + c_time_real_x2[2][:2])
            c_date_real_x = f_real_x[3].split(':')
            c_date_real.append(c_date_real_x[1].strip())
        elif len(c_time_real_x1) == 2:
            c_time_real_x2 = f_real_x[4].split(':')
            c_time_real_x3 = c_time_real_x2[2].split('(')
            c_time_real.append(c_time_real_x2[1].strip() + ':' + c_time_real_x3[0][:2])
            c_date_real_x = c_time_real_x3[1].split(')')
            c_date_real.append(c_date_real_x[0].strip())
        else:
            c_time_real.append('-')
            c_date_real.append('-')
        c_gate_x = f_real_x[6].split(':')
        c_gate.append(c_gate_x[1].strip())
    # Option 2: Arrival
    elif c_ftype[i] == 'Arrival':
        link_all = link_arr_ini + fnr + link_fi
        html = urlopen(link_all)
        bs = BeautifulSoup(html.read(), 'html.parser')
        f_real = bs.find(id='flight_arr')
        f_real_x = f_real.get_text().split('\n')
        c_time_real_x1 = f_real_x[4].split('(')
        if len(c_time_real_x1) == 1:
            c_time_real_x2 = f_real_x[4].split(':')
            c_time_real.append(c_time_real_x2[1].strip() + ':' + c_time_real_x2[2][:2])
            c_date_real_x = f_real_x[3].split(':')
            c_date_real.append(c_date_real_x[1].strip())
        elif len(c_time_real_x1) == 2:
            c_time_real_x2 = f_real_x[4].split(':')
            c_time_real_x3 = c_time_real_x2[2].split('(')
            c_time_real.append(c_time_real_x2[1].strip() + ':' + c_time_real_x3[0][:2])
            c_date_real_x = c_time_real_x3[1].split(')')
            c_date_real.append(c_date_real_x[0].strip())
        else:
            c_time_real.append('-')
            c_date_real.append('-')
        c_gate_x = f_real_x[5].split(':')
        c_gate_x2 = c_gate_x[1].split('\t')
        c_gate.append(c_gate_x2[0].strip())
    else:
        c_time_real.append('-')
        c_date_real.append('-')
        c_gate.append('-')
    i = i+1
    time.sleep(0.5) #added a delay

# dataframe creation
df = pd.DataFrame(data = list(zip(c_fdate, c_fdest_city, c_fdest_iata, c_fair, c_fnum, c_ftype, c_fhour, 
                                           c_fterm, c_fstatus_all, c_date_real, c_time_real, c_gate)), 
                      columns = ['Scheduled Date', 'City', 'IATA', fair[0].get_text(), fnum[0].get_text(), 'Operation',
                                 'Scheduled Time', fterm[0].get_text(), fstatus_all[0].get_text(), 'Real Date', 'Real Time', 'Gate'])

# Saving the file
currentDir = os.path.dirname(__file__)
fileName = 'BCN_Operations_' + c_fdate[0] + '.csv'
filePath = os.path.join(currentDir, fileName)
df.to_csv(filePath)
