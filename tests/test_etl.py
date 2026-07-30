import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
from src.etl_bloomberg import silver_clean

def test_etf_close6_null_fallback():
    df = pd.DataFrame([{'ticker':'HDLV','trade_date':'2025-07-10',
        'close_price':80.5,'close6':None,'close1':80.0,'volume':10000}])
    result = silver_clean(df)
    assert result.iloc[0]['close6'] == 80.0
    assert result.iloc[0]['dq_flag'] == 'close6_null_fallback'

def test_negative_price_filtered():
    df = pd.DataFrame([{'ticker':'IBM','trade_date':'2025-07-10',
        'close_price':-5.0,'close6':100.0,'close1':100.0,'volume':20000}])
    assert len(silver_clean(df)) == 0

def test_dedup():
    row = {'ticker':'AAPL','trade_date':'2025-07-10','close_price':185.5,'close6':185.0,'close1':185.0,'volume':50000}
    assert len(silver_clean(pd.DataFrame([row,row]))) == 1