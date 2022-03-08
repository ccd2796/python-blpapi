# -*- coding: utf-8 -*-
import datetime
from bloomberg import BDH

#Securities and fields must be passed as a list
securities = ['AAPL US Equity','C US Equity']

#For a complete list of available fields, use FLDS when loading a security in Bloomberg.
fields = ['PX_LAST', 'PX_VOLUME']

# Dates are used in %Y%m%d format (e.g. 20220306 for March 6th 2022).
# Suggested use is with datetime:
date_ini = datetime.date(2021,6,1).strftime("%Y%m%d")
date_end = datetime.date(2021,6,30).strftime("%Y%m%d")

#Settings
# Complete list of settings can be found in the "BLPAPI Core 
# Developer Guide", section "15.4. BDH(): HISTORICAL “END-OF-DAY” DATA (STATIC)"
settings = {"periodicityAdjustment":"ACTUAL",
            "periodicitySelection":"DAILY",
            "startDate": date_ini,
            "endDate": date_end,
            "nonTradingDayFillOption":"NON_TRADING_WEEKDAYS",
            "nonTradingDayFillMethod":"PREVIOUS_VALUE",
            } 

df_bdh = BDH(securities, fields, settings)