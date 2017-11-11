def get_json_data(json_url, cache_path):
    import pickle
    import pandas as pd
    '''Download and cache JSON data, return as a dataframe.'''
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)
        print('Loaded {} from cache'.format(json_url))
    except (OSError, IOError) as e:
        print(e.message)
        print('Downloading {}'.format(json_url))
        df = pd.read_json(json_url)
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(json_url, cache_path))
    return df

def get_crypto_data(poloniex_pair, base_polo_url, start_date, end_date, period):
    '''Retrieve cryptocurrency data from poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), period)
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')
    return data_df

def load_data(poloniex_pair):
    from datetime import datetime
    base_polo_url = \
        'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
    start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
    end_date = datetime.now() # up until today
    period = 86400 # pull daily data (86,400 seconds per day)

    data_df = get_crypto_data(
        poloniex_pair, base_polo_url, start_date, end_date, period
    )

    return data_df

def get_quandl_data(quandl_id):
    import quandl
    import pickle
    '''Download and cache Quandl dataseries'''
    cache_path = '{}.pkl'.format(quandl_id).replace('/','-')
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)
        print('Loaded {} from cache'.format(quandl_id))
    except (OSError, IOError) as e:
        print(e.message)
        print('Downloading {} from Quandl'.format(quandl_id))
        df = quandl.get(quandl_id, returns="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df

def get_averaged_btc(fiat = 'EUR'):
    from data_processing import merge_dfs_on_column, clean_data

    exchanges = ['COINBASE','BITSTAMP','ITBIT', 'KRAKEN']

    exchange_data = {}

    for exchange in exchanges:
        exchange_code = 'BCHARTS/{0}{1}'.format(exchange, fiat)
        btc_exchange_df = get_quandl_data(exchange_code)
        exchange_data[exchange] = btc_exchange_df

    btc_fiat_datasets = merge_dfs_on_column(
        list(
            exchange_data.values()
        ),
        list(
            exchange_data.keys()
        ),
        'Weighted Price'
    )

    return clean_data(btc_fiat_datasets)


