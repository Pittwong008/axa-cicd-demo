# src/etl_bloomberg.py
import pandas as pd
import datetime


def bronze_ingestion(file_path):
    df = pd.read_json(file_path)
    df['ingestion_ts'] = datetime.datetime.now().isoformat()
    df['pipeline_run_id'] = '{{RUN_ID}}'
    print(f"[Bronze] {len(df)} rows")
    return df


def silver_clean(df):
    df = df.drop_duplicates(subset=['ticker', 'trade_date'])
    if 'close6' in df.columns and 'close1' in df.columns:
        mask = df['close6'].isnull()
        df.loc[mask, 'close6'] = df.loc[mask, 'close1']
        df.loc[mask, 'dq_flag'] = 'close6_null_fallback'
    df = df[df['close_price'] > 0]
    print(f"[Silver] {len(df)} rows")
    return df


def gold_model(df):
    df['market_value'] = df['close_price'] * df['volume']
    df['processing_date'] = datetime.date.today().isoformat()
    print(f"[Gold] {len(df)} rows")
    return df
