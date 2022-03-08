# -*- coding: utf-8 -*-
from bloomberg import BDP

#Securities and fields must be passed as a list
securities = ['AAPL US Equity','C US Equity']

#For a complete list of available fields, use FLDS when loading a security in Bloomberg.
fields = ['NAME', 'GICS_INDUSTRY_NAME', 'CRNCY_ADJ_PX_LAST']

df_bdp = BDP(securities, fields)

#Example with overrides
override = {'EQY_FUND_CRNCY':'EUR'}
df_bdp_override = BDP(securities, fields, override)