# -*- coding: utf-8 -*-
"""
.

Simple wrapper for blpapi library to Pandas. Resembles BDH, BDP and BDS Bloomberg-Excel functions. Can only be used in a Bloomberg Terminal. Requires blpapi, which can be installed in cmd via "python -m pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi".

@author: ccd
"""
import blpapi
import pandas as pd
import numpy as np 
import datetime

def BDH(securities, fields, settings, override = None, debug = False):
    """
    Parameters
    ----------
    securities : List
        Securities identifier must be passed as a list.
    fields : List
        Fields must be passed as a list.
    settings : Dict
        Settings must be passed as a dict. Complete list of settings can be found in the BLPAPI Core Developer Guide, section 15.4. BDH(): HISTORICAL “END-OF-DAY” DATA (STATIC).
    override : Dict, optional
        Override for fields (if any) must be passed as a dict. The default is None.
    debug : Boolean, optional
        If True, prints the complete blpapi response message. The default is False.
        
    For a complete list of fields and overrides, use FLDS when loading a security in Bloomberg.
    

    Returns
    -------
    df_output : DataFrame
        Outputs a DataFrame multiindex object. Tickers in first row index and fields in second row index. Column index are dates.

    """
    if type(securities) != list or type(fields) != list:
        print('Securities and fields must be passed as lists.')
        raise TypeError
    
    
    session = blpapi.Session()
    session.start()
    session.openService("//blp/refdata")
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("HistoricalDataRequest")
    
    for sec in securities:
        request.getElement("securities").appendValue(sec)
    for fld in fields:
        request.getElement("fields").appendValue(fld)
    for setting in settings:
        request.set(setting, settings[setting])
    if override:
        overrides = request.getElement("overrides")
        dict_over = {}
        for o in override:
            dict_over[o] = overrides.appendElement()
            dict_over[o].setElement("fieldId", o)
            dict_over[o].setElement("value", override[o])
        
    
    session.sendRequest(request)
    
    respuesta = []
    # Process received events
    a = 0
    while(True):
        # We provide timeout to give the chance for Ctrl+C handling:
        ev = session.nextEvent(500)
        for msg in ev:
            if debug:
                print(msg)
            if a > 2:
                respuesta.append(msg)
    
        a += 1
        if ev.eventType() == blpapi.Event.RESPONSE:
            # Response completly received, so we could exit
            break
        
    df_list = []
    for rpta in respuesta:
        data_dict = {}
       
        security = rpta.getElement('securityData').getElement('security').getValueAsString().split("\n")[0]
        rpta_val = rpta.getElement('securityData').getElement('fieldData')
        
        #lenght = len(list(rpta_val.values()))
        fields_copy = fields.copy()
        fields_copy.insert(0,'date')
        #for fld in rpta_val.getValue(lenght-1).elements():
        #    data_dict[str(fld.name())] = []
        for fld in fields_copy:
            data_dict[fld] = []
        
        for rpta_field in rpta_val.values():
            for key in data_dict.keys():
                #print(key)
                try:
                    fld = rpta_field.getElement(key)
                except:
                    data_dict[key].append(np.nan)
                else: 
                    data_dict[key].append(fld.getValue())
    
        tuples = []
        for fld in data_dict:
             if fld != 'date': tuples.append((security,fld)) 
             #tuples.append((security,fld))
        mix = pd.MultiIndex.from_tuples(tuples, names=["Ticker", "Field"])
        
        df = pd.DataFrame.from_dict(data = data_dict).set_index('date').T.set_index(mix).T
        df.index =  pd.to_datetime(df.index, format='%Y-%m-%d')
        df_list.append(df)
    
    df_output = df_list[0]
    if len(df_list) > 1:
        for i in range(1,len(df_list)):
            df_output = df_output.merge(df_list[i], how='outer', on='date')
    
    df_output = df_output.sort_values(by=['date'])
    session.stop()
    return df_output



def BDP(securities, fields, override = None, debug = False):
    """
    Parameters
    ----------
    securities : List
        Securities identifier must be passed as a list.
    fields : List
        Fields must be passed as a list.
    override : Dict, optional
        Override for fields (if any) must be passed as a dict. The default is None.
    debug : Boolean, optional
        If True, prints the complete blpapi response message. The default is False.
        
    For a complete list of fields and overrides, use FLDS when loading a security in Bloomberg.
    

    Returns
    -------
    df_output : DataFrame
        Outputs a DataFrame object. Tickers as index and fields as columns.

    """
    if type(securities) != list or type(fields) != list:
        print('Securities and fields must be passed as lists.')
        raise TypeError
    
    
    session = blpapi.Session()
    session.start()
    session.openService("//blp/refdata")
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("ReferenceDataRequest")
    
    for sec in securities:
        request.getElement("securities").appendValue(sec)
    for fld in fields:
        request.getElement("fields").appendValue(fld)
    if override:
        overrides = request.getElement("overrides")
        dict_over = {}
        for o in override:
            dict_over[o] = overrides.appendElement()
            dict_over[o].setElement("fieldId", o)
            dict_over[o].setElement("value", override[o])
    
    session.sendRequest(request)
    
    respuesta = []
    # Process received events
    a = 0
    while(True):
        # We provide timeout to give the chance for Ctrl+C handling:
        ev = session.nextEvent(500)
        for msg in ev:
            if debug:
                print(msg)
            if a>2:
                respuesta.append(msg)
    
        a += 1
        if ev.eventType() == blpapi.Event.RESPONSE:
            # Response completly received, so we could exit
            break
        
    data_dict = {}
    
    for full_rpta in respuesta:
        for rpta in full_rpta.getElement('securityData').values():
            security = rpta.getElement('security').getValueAsString().split("\n")[0]
            field_dict = {}
            field_list = []
            data_dict[security] = []
            for field in rpta.getElement('fieldData').elements():
                field_list.append(field.name())
                field_dict[str(field.name())] = field.getValue()
            for f in fields:
                if f in field_list:
                    data_dict[security].append(field_dict[f])
                else:
                    data_dict[security].append(np.nan)
    
    df = pd.DataFrame.from_dict(data_dict, orient='index', columns=fields)
    session.stop()
    return df


def BDS(securities, fields, override = None, debug = False):
    """
    Parameters
    ----------
    securities : List
        Securities identifier must be passed as a list.
    fields : List
        Field must be passed as a list. Only accepts 1 field.
    override : Dict, optional
        Override for fields (if any) must be passed as a dict. The default is None.
    debug : Boolean, optional
        If True, prints the complete blpapi response message. The default is False.
        
    For a complete list of fields and overrides, use FLDS when loading a security in Bloomberg.
    
    
    Returns
    -------
    df_output : DataFrame
        If a single security is passed, output is a DataFrame. Otherwise, output is a dictionary containing DataFrames. Indices depend on securities and fields consulted.

    """
    if type(securities) != list or type(fields) != list:
        print('Securities and fields must be passed as lists.')
        raise TypeError
        
    if len(fields) > 1:
        print('BDS only accepts 1 field. Separated queries are required for multiple fields.')
        raise ValueError

    session = blpapi.Session()
    session.start()
    session.openService("//blp/refdata")
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("ReferenceDataRequest")
        
    for sec in securities:
        request.getElement("securities").appendValue(sec)
    for fld in fields:
        request.getElement("fields").appendValue(fld)
    if override:
        overrides = request.getElement("overrides")
        dict_over = {}
        for o in override:
            dict_over[o] = overrides.appendElement()
            dict_over[o].setElement("fieldId", o)
            dict_over[o].setElement("value", override[o])
            
    session.sendRequest(request)
    
    respuesta = []
    # Process received events
    a = 0
    while(True):
        # We provide timeout to give the chance for Ctrl+C handling:
        ev = session.nextEvent(500)
        for msg in ev:
            if debug:
                print(msg)
            if a>2:
                respuesta.append(msg)
    
        a += 1
        if ev.eventType() == blpapi.Event.RESPONSE:
            # Response completly received, so we could exit
            break
         
    df_dict = {}
    
    for full_rpta in respuesta:
        for rpta in full_rpta.getElement('securityData').values():
            security = rpta.getElement('security').getValueAsString().split("\n")[0]
            data_dict = {}
            i = 0
            for tenor in rpta.getElement('fieldData').getElement(fields[0]).values():
                data_dict[i] = {}
                for flds in tenor.elements():
                    if flds.isNull():
                        del data_dict[i]
                        i-=1
                        break
                    else:
                        data_dict[i][str(flds.name())] = flds.getValue()
                i+=1

            df = pd.DataFrame.from_dict(data_dict, orient='index')
            df_dict[security] = df
            
    session.stop()
    
    if len(df_dict) == 1:
        return df_dict[securities[0]]
    else:
        return df_dict


def BDHIB(security, eventType, interval, startDateTime, endDateTime, gapFillInitialBar = False, settings = None, debug = False):
    """
    Parameters
    ----------
    security : String
        Security identifier must be passed as a string.
    eventType : String
        Market event must be passed as a string. Can be TRADE, BID or ASK.
    interval : int
        Sets the lenght of each time-bar in minutes. Must be an integer between 1 and 1,440 (24 hours).
    startDateTime, endDateTime: datetime
        Sets the start and end points for the request. Must be passed as datetime objects.
    gapFillInitialBar: Boolean (Default False)
        If true, forces an initial bar on the startDateTime point with the last price available.
    settings : Dict, optional (Default None)
        Settings must be passed as a dict. Complete list of settings can be found in the BLPAPI Core Developer Guide, section 15.6. BDH()/BRB(): INTRADAY BAR DATA (STATIC/SUBSCRIPTION).
    debug : Boolean, optional (Default False)
        If True, prints the complete blpapi response message. The default is False.

    Returns
    -------
    df_output : DataFrame
        Outputs a DataFrame object. Index are dates and times.
        
        Columns are:
            OPEN: Open price of bar
            HIGH: Highest price of bar
            LOW: Lowest price of bar
            CLOSE: Last price of bar
            TICKS: Number of ticks in bar
            VOLUME: Volume traded in bar
        
    """
    if type(security) != str or type(eventType) != str:
        print('Security and eventType must be passed as strings.')
        raise TypeError
        
    if eventType not in ["TRADE", "BID", "ASK"]:
        print("Event type must be TRADE, BID or ASK")
        raise ValueError
    
    session = blpapi.Session()
    session.start()
    session.openService("//blp/refdata")
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("IntradayBarRequest")
    
    time_offset = datetime.datetime.now() - datetime.datetime.utcnow()
    
    request.set('security', security)
    request.set('eventType', eventType)
    request.set('interval', interval)
    request.set('startDateTime', startDateTime - time_offset)
    request.set('endDateTime', endDateTime - time_offset)
    request.set('gapFillInitialBar', gapFillInitialBar)
    
    if settings:
        for setting in settings:
            request.set(setting, settings[setting])
        
    BAR_DATA = blpapi.Name("barData")
    BAR_TICK_DATA = blpapi.Name("barTickData")
    OPEN = blpapi.Name("open")
    HIGH = blpapi.Name("high")
    LOW = blpapi.Name("low")
    CLOSE = blpapi.Name("close")
    VOLUME = blpapi.Name("volume")
    NUM_EVENTS = blpapi.Name("numEvents")
    TIME = blpapi.Name("time")
    
    session.sendRequest(request)
    
    respuesta = []
    # Process received events
    a = 0
    while(True):
        # We provide timeout to give the chance for Ctrl+C handling:
        ev = session.nextEvent(500)
        for msg in ev:
            if debug:
                print(msg)
            if a > 2:
                respuesta.append(msg)
    
        a += 1
        if ev.eventType() == blpapi.Event.RESPONSE:
            # Response completly received, so we could exit
            break
        
    data_dict = {}
    for rpta in respuesta:
        bars = rpta.getElement(BAR_DATA).getElement(BAR_TICK_DATA).values()
        
        for bar in bars:
            time = bar.getElementAsDatetime(TIME) + time_offset
            px_open = bar.getElementAsFloat(OPEN)
            px_high = bar.getElementAsFloat(HIGH)
            px_low = bar.getElementAsFloat(LOW)
            px_close = bar.getElementAsFloat(CLOSE)
            numEvents = bar.getElementAsInteger(NUM_EVENTS)
            volume = bar.getElementAsInteger(VOLUME)
            
            data_dict[time] = {'OPEN': px_open,
                               'HIGH': px_high,
                               'LOW': px_low,
                               'CLOSE': px_close,
                               'TICKS': numEvents,
                               'VOLUME': volume
                               }
            
    cols = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKS', 'VOLUME']
    
    session.stop()
    return pd.DataFrame.from_dict(data_dict, orient='index', columns=cols)
