from functions import daily_close,get_all_tickers

list_all = get_all_tickers()
for i in list_all:
    try:
        daily_close(i)
    except KeyError:
        continue