# -*- coding: utf-8 -*-
import datetime
from bloomberg import BDHIB

#Security and Event must be passed as strings.
security = "USDPEN Curncy"

#Event can be TRADE, BID or ASK.
eventType = "TRADE"

#lenght of each time-bar in minutes. Must be an integer between 1 and 1,440 (24 hours).
interval = 5

#Start and end points must be passed as datetime objects.
startDateTime = datetime.datetime(2022, 5, 25, 0, 0, 0)
endDateTime = datetime.datetime(2022, 5, 28, 0, 0, 0)

#gapFillInitialBar (optional): If true, forces an initial bar on startDateTime with last price avaiable. Default is False.
gapFillInitialBar = True

#settings must be passed as dict. Complete list and descripion of settings can be found in the BLPAPI Core Developer Guide,
#section 15.6. BDH()/BRB(): INTRADAY BAR DATA (STATIC/SUBSCRIPTION).
# settings = {'adjustmentSplit':True,
#             'adjustmentAbnormal':True,
#             'adjustmentNormal': True,
#             'adjustmentFollowDPDF': True}

df_bdhib = BDHIB(security, eventType, interval, startDateTime, endDateTime, gapFillInitialBar)

