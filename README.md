# Yahoo-Finance-Data-Gathering
# get financial historical data from yahoo, including open, high, low, close, adjusted close and volume

get(yahoo_code,inicio,fin)

Where:
yahoo_code=str - ticker symbol from yahoo finance (for instance 'GOOG' for Google stocks as quoted in NasdaqGS)
inicio=tuple - (yyyy,mm,dd) starting date
fin=tuple - (yyyy,mm,dd) ending date
