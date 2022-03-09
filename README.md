# python-blpapi

Simple wrapper for blpapi library to Pandas. Resembles BDH, BDP and BDS Bloomberg-Excel functions. Can only be used in a Bloomberg Terminal. Requires blpapi.

```python
#To install blpapi, run in cmd

python -m pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
```


# Examples

## BDP
+ Securities and fields must be passed as lists
+ Overrides (if any) must be passed as dict
+ Output is a DataFrame


```python
from bloomberg import BDP

#Securities and fields must be passed as a list
securities = ['AAPL US Equity','C US Equity']

#For a complete list of available fields, use FLDS when loading a security in Bloomberg.
fields = ['NAME', 'GICS_INDUSTRY_NAME', 'CRNCY_ADJ_PX_LAST']

df_bdp = BDP(securities, fields)

#Example with overrides
override = {'EQY_FUND_CRNCY':'EUR'}
df_bdp_override = BDP(securities, fields, override)
```
df_bdp  
| Index          | NAME           | GICS_INDUSTRY_NAME  | CRNCY_ADJ_PX_LAST |
| -------------  |-------------| -----| ----|
| AAPL US Equity | APPLE INC        | Technology Hardware, Storage & | 157.44 |
| C US Equity    | CITIGROUP INC      |   Banks | 54.87|  

<br/>

df_bdp_override
| Index          | NAME           | GICS_INDUSTRY_NAME  | CRNCY_ADJ_PX_LAST |
| -------------  |-------------| -----| ----|
| AAPL US Equity | APPLE INC        | Technology Hardware, Storage & | 144.321 |
| C US Equity    | CITIGROUP INC      |   Banks | 50.2979| 


## BDH
```python
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
```

df_bdh.head(5)
| Ticker          | AAPL US Equity           | AAPL US Equity  | C US Equity | C US Equity |
| -------------   |-------------             | -----           | ----        |    ---     |
| Field | PX_LAST        | PX_VOLUME | PX_LAST | PX_VOLUME |
| date  |                |           |         |           |
| 2021-06-01  |     124.28           |     67637118.0      |     79.76    |    15450506.0       |



## BDS
```python
import datetime
from bloomberg import BDS

#Securities and fields must be passed as a list:
securities = ['YCSW0042 Index', 'YCSW0141 Index']

# Only accepts 1 field.
# For a complete list of available fields, use FLDS when loading a security in Bloomberg.
fields = ['CURVE_TENOR_RATES']

df_bds = BDS(securities, fields)

#Example with overrides:
# Dates are used in %Y%m%d format (e.g. 20220306 for March 6th 2022).
# Suggested use is with datetime:
date = datetime.date(2021,6,12).strftime("%Y%m%d")
override = {'CURVE_DATE':date}
df_bds_override = BDS(securities, fields, override) 
```
