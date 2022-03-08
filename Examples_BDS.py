# -*- coding: utf-8 -*-
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
