import pandas as pd
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Dropout
from keras.models import Sequential
from datetime import datetime, timedelta

# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    args = config()
    
    model_con_name='model_con.hdf5'
    model_gen_name='model_gen.hdf5'

    if not os.path.exists(model_con_name):
        model = Sequential()
        model.add(Dense(168, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(336, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(48, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(24, activation='relu'))
        model.compile(loss="mse", optimizer="adam", metrics=['mse'])
        training_data = os.listdir('training_data')
        X_con = []
        Y_con = []

        X_gen = []
        Y_gen = []

        for target in training_data:
            df = pd.read_csv('training_data/' + target)
            for i in range(int(df.shape[0] / 24 - 7)):
                X_con.append(df.loc[i * 24 : (i + 7) * 24 - 1, 'consumption'].tolist())
                Y_con.append(df.loc[(i + 7) * 24 : (i + 8) * 24 - 1, 'consumption'].tolist())
                
                X_gen.append(df.loc[i * 24 : (i + 7) * 24 - 1, 'generation'].tolist())
                Y_gen.append(df.loc[(i + 7) * 24 : (i + 8) * 24 - 1, 'generation'].tolist())
        
        X_con = np.array(X_con)
        Y_con = np.array(Y_con)
        X_gen = np.array(X_gen)
        Y_gen = np.array(Y_gen)
        
        history_con = model.fit(
            X_con,
            Y_con,
            batch_size=64,
            epochs=1000,
            validation_split=0.2
        )
        model.save(model_con_name)
        
        history_con = model.fit(
            X_gen,
            Y_gen,
            batch_size=64,
            epochs=1000,
            validation_split=0.2
        )
        model.save(model_gen_name)
    else:
        model_con = keras.models.load_model(model_con_name)
        model_gen = keras.models.load_model(model_gen_name)

    df_bid = pd.read_csv(args.bidresult)
    df_con = pd.read_csv(args.consumption)
    df_gen = pd.read_csv(args.generation)

    buy_price = 2.47
    sell_price = 2.57

    df_bid = df_bid.loc[:, ['action', 'trade_price', 'status']]
    for i in range(df_bid.shape[0]):
        if df_bid.loc[i, 'status'] == '完全成交':
            if df_bid.loc[i, 'action'] == 'buy' and buy_price > df_bid.loc[i, 'trade_price']:
                buy_price = df_bid.loc[i, 'trade_price'] - 0.01
            elif df_bid.loc[i, 'action'] == 'sell' and sell_price < df_bid.loc[i, 'trade_price']:
                sell_price = df_bid.loc[i, 'trade_price'] + 0.01

        elif df_bid.loc[i, 'status'] == '部分成交':
            if df_bid.loc[i, 'action'] == 'buy' and buy_price > df_bid.loc[i, 'trade_price']:
                buy_price = df_bid.loc[i, 'trade_price']
            elif df_bid.loc[i, 'action'] == 'sell' and sell_price < df_bid.loc[i, 'trade_price']:
                sell_price = df_bid.loc[i, 'trade_price']
        else:
            if df_bid.loc[i, 'action'] == 'buy' and buy_price > df_bid.loc[i, 'trade_price']:
                buy_price = df_bid.loc[i, 'trade_price'] + 0.01
            elif df_bid.loc[i, 'action'] == 'sell' and sell_price < df_bid.loc[i, 'trade_price']:
                sell_price = df_bid.loc[i, 'trade_price'] - 0.01

    X_con = df_con.loc[:, 'consumption'].tolist()
    X_gen = df_gen.loc[:, 'generation'].tolist()

    Y_con = model_con.predict([X_con])[0]
    Y_gen = model_gen.predict([X_gen])[0]

    y = Y_con - Y_gen

    current_time = datetime.strptime(df_con.loc[167, 'time'], "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)

    data = []

    for need in y:
        if round(need) > 0:
            data.append([datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S'), 'buy', 2.47, round(need)])
        elif round(need) < 0:
            data.append([datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S'), 'sell', 2.57, round(need)])
        current_time = current_time + timedelta(hours=1)

    output(args.output, data)