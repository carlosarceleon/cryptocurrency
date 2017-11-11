import sys

def main(argv):
    from altcoinlist import altcoints_to_get
    from load_funcs import load_data
    from data_processing import add_fiat_column
    from load_funcs import get_averaged_btc, merge_dfs_on_column

    FIAT_TO_PROCESS = 'EUR'

    fiat = FIAT_TO_PROCESS

    altcoin_list = altcoints_to_get()

    altcoin_data = {}

    btc_fiat_datasets = get_averaged_btc(fiat)

    for altcoin in altcoin_list:
        coinpair = 'BTC_{}'.format(altcoin)
        crypto_price_df = load_data(coinpair)

        altcoin_data[altcoin] = crypto_price_df

    altcoin_data = add_fiat_column( altcoin_data, btc_fiat_datasets )

    combined_altcoin_df = merge_dfs_on_column(
        list(altcoin_data.values()),
        list(altcoin_data.keys()),
        'price_{}'.format(fiat)
    )

    combined_altcoin_df['BTC'] = btc_fiat_datasets('avg_btc_price_{}'.format(fiat))


if __name__=="__main__":
    main(sys.argv)
