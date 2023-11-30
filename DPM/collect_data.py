import pickle

import yfinance as yf
import numpy as np

def get_stock_data(tickers, start_date, end_date):
    gathered_whole_data = list()
    min_data_ticker = tickers[0]
    min_num_data = 9999999999
    no_min_data = False
    for ticker in tickers:
        gathered_ticker_data = list()
        data = yf.download(ticker, start=start_date, end=end_date)
        date_time = data['Open'].keys().strftime('%Y-%m-%d %H:%M:%S')
        values = data[["High", "Low", "Open", "Close", "Volume", "Adj Close"]].values.tolist()
        for t, v in zip(date_time, values):
            v.insert(0, t)
            gathered_ticker_data.append(v)
        gathered_ticker_data = np.array(gathered_ticker_data)
        if min_num_data != 9999999999 and min_num_data == gathered_ticker_data.shape[0]:
            no_min_data = False
        elif min_num_data >= gathered_ticker_data.shape[0]:
            min_data_ticker = ticker
            no_min_data = True
        else:
            raise Exception('???')
        gathered_whole_data.append(gathered_ticker_data)
    if no_min_data:
        checked_gathered_whole_data = list()
        min_data_index = tickers.index(min_data_ticker)
        check_date_times = gathered_whole_data[min_data_index]
        check_date_times = check_date_times[:, 0]
        for ticker_data in gathered_whole_data:
            checked_date_times = list()
            for ticker_date_time in ticker_data[:, 0]:
                if ticker_date_time in check_date_times:
                    checked_date_times.append(True)
                else:
                    checked_date_times.append(False)
            checked_ticker_data = ticker_data[checked_date_times]
            checked_gathered_whole_data.append(np.array(checked_ticker_data))
        return np.array(checked_gathered_whole_data)
    return np.array(gathered_whole_data)

if __name__ == '__main__':
    tickers = ['GOOG', 'NVDA', 'AMZN', 'AMD', 'QCOM', 'INTC', 'MSFT', 'AAPL', 'BIDU']
    file_name = 'stock_decrease.pickle'  # 'stock_increase.pickle', 'stock_no_change.pickle', 'stock_decrease.pickle'
    start_date = '2001-02-20' # '2006-10-20', '2003-06-20', '2001-02-20'
    end_date = '2009-05-21' # '2013-11-21', '2011-08-21', '2009-05-21'
    data = get_stock_data(tickers, start_date, end_date)
    print(data.shape)
    print(data[0, 0, :])
    save_path = '/home/link/git/rl_portfolio_management/DPM/pgportfolio/data/' + file_name
    # np.save(save_path, data)
    with open(save_path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
