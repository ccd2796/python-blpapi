# python-blpapi

Simple wrapper for blpapi library to Pandas. Resembles BDH, BDP and BDS Bloomberg-Excel functions for historical data. Can only be used in a logged Bloomberg Terminal. Requires blpapi.

```python
#To install blpapi, run in cmd

python -m pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
```


# Examples

## BDP
+ Securities and fields must be passed as lists.
+ For a complete list of fields and overrides, use FLDS when loading a security in Bloomberg.
+ Overrides (if any) must be passed as dict.
+ Output is a DataFrame. Tickers as index, fields as column names.


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
+ Securities and fields must be passed as lists.
+ For a complete list of fields and overrides, use FLDS when loading a security in Bloomberg.
+ Overrides (if any) must be passed as dict.
+ Output is a multiindex DataFrame. Tickers as first row index, fields as second row index. Column index contains dates.
+ Complete list of settings can be found in the "BLPAPI Core Developer Guide", section "15.4. BDH(): HISTORICAL “END-OF-DAY” DATA (STATIC)"

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
| -------------:   |-------------:             | -----:           | ----:        |    ---:     |
| Field | PX_LAST        | PX_VOLUME | PX_LAST | PX_VOLUME |
| date  |                |           |         |           |
| 2021-06-01  |     124.28           |     67637118.0      |     79.76    |    15450506.0       |
| 2021-06-02  |     125.06           |     59278862.0      |     79.86    |    15285588.0       |
| 2021-06-03  |     123.54           |     76229170.0      |     79.63    |    22255785.0       |
| 2021-06-04  |     125.89           |     75169343.0      |     79.49    |    13806958.0       |
| 2021-06-07  |     125.90           |     71057550.0      |     79.31    |    12670074.0       |


## BDS
+ Securities must be passed as a list. Only accepts 1 field.
+ For a complete list of fields and overrides, use FLDS when loading a security in Bloomberg.
+ Overrides (if any) must be passed as dict.
+ If a single security is passed, output is a DataFrame. Otherwise, output is a dictionary containing DataFrames. Indices depend on securities and fields consulted.

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
df_bds['YCSW0042 Index'].head(5)

|           | Tenor   | Ticker  | Ask Yield | Mid Yield | Bid Yield | Last Update |
| :-------------   |-------------:   | -----:           | ----:        |    ---:     | ---: | :--- | 
|0  |  1D    |   FEDL01 Index  |    0.080  |    0.080   |   0.080|  2022-03-08|
|1  |  1W | USSO1Z BGN Curncy |     0.155   |   0.133   |   0.111 | 2022-03-08|
|2  |  2W | USSO2Z BGN Curncy   |   0.237   |   0.230  |    0.224 | 2022-03-08|
|3  |  3W | USSO3Z BGN Curncy   |   0.275  |    0.265  |    0.255 | 2022-03-08|
|4  |  1M |  USSOA BGN Curncy   |   0.291 |     0.287  |    0.284|  2022-03-08|


<br/>

df_bds_override['YCSW0042 Index'].head(5)

|           | Tenor   | Ticker  | Ask Yield | Mid Yield | Bid Yield | Last Update |
| :-------------   |-------------:   | -----:           | ----:        |    ---:     | ---: | :--- | 
|0  |  1D |      FEDL01 Index    |  0.060    |  0.060   |   0.060 | 2021-06-11|
|1  |  1W | USSO1Z BGN Curncy    |  0.071    |  0.067   |   0.063 | 2021-06-11|
|2  |  2W | USSO2Z BGN Curncy    |  0.073    |  0.070   |   0.067 | 2021-06-11|
|3  |  3W | USSO3Z BGN Curncy    |  0.075     | 0.067   |   0.059 | 2021-06-11|
|4  |  1M |  USSOA BGN Curncy    |  0.074     | 0.070   |   0.066 | 2021-06-11|
