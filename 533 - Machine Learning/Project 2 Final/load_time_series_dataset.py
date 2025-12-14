# =========================================
# source: https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014
# =========================================

import pandas as pd
import numpy as np

# =========================================
# 1. Load and convert to hourly
# =========================================

def filter_clients_by_zero_ratio(df_hourly, max_zero_ratio):
    zero_counts = (df_hourly == 0).sum(axis=0)           # count zeros per column
    zero_ratio = zero_counts / len(df_hourly)            # ratio per client
    keep_cols = zero_ratio[zero_ratio <= max_zero_ratio].index
    return df_hourly[keep_cols], zero_ratio

def load_hourly_df(file_path):
    """
    Loads LD2011_2014.txt and returns an hourly-aggregated DataFrame:
        index: hourly timestamps
        columns: 370 clients, values are kWh per hour (sum of 4x 15-min kW)
    """
    df_raw = pd.read_csv(
        file_path,
        sep=';',           # semicolon separated
        decimal=',',       # comma decimal separator
        parse_dates=[0],   # first column = datetime
        index_col=0,
        low_memory=False
    )

    # Ensure numeric columns
    df_raw = df_raw.apply(pd.to_numeric, errors='coerce')
    df_raw.sort_index(inplace=True)

    # Convert 15-min (kW) -> hourly (kWh per hour)
    df_hourly = df_raw.resample('h').sum()

    return df_hourly

def make_supervised_from_clients_multi(df_clients, in_window=48, out_horizon=24):
    """
    Convert multiple client time series into a multi-step supervised dataset.

    Parameters
    ----------
    df_clients : pd.DataFrame
        Shape (T, N_clients). Each column is one client's hourly load series.
        Index should be a DateTimeIndex (hourly).
    in_window : int, default=168
        Number of past hours used as input (look-back window).
    out_horizon : int, default=24
        Number of future hours to predict (forecast horizon).

    Supervised formulation
    ----------------------
    For EACH client (each column), build samples:

        Input X row:  [load_{t-in_window}, ..., load_{t-2}, load_{t-1}]
        Target y row: [load_{t}, load_{t+1}, ..., load_{t+out_horizon-1}]

    So with in_window=168 and out_horizon=24, each sample uses the past
    168 hours to predict the next 24 hours.

    Returns
    -------
    X : np.ndarray
        Shape (n_samples_total, in_window)
        Each row is one input window (flattened past values).
    Y : np.ndarray
        Shape (n_samples_total, out_horizon)
        Each row is the next out_horizon loads for that client.
    df_supervised : pd.DataFrame
        Columns:
            - 'client_id'
            - 'time'       (timestamp of the FIRST predicted hour)
            - 'target_i' .. 'target_out_horizon'
            - 'step_i' .. 'step_in_window' (oldest to newest in the input window)
    """
    X_list, Y_list = [], []
    client_list, time_list = [], []

    stride_time = in_window+out_horizon # must use in_window+out_horizon for test
    
    index = df_clients.index

    for col in df_clients.columns:

        series = df_clients[col].astype(float).values
        T = len(series)

        for t in range(in_window, T - out_horizon + 1, stride_time):
            x_window = series[t-in_window:t]                  # (in_window,)
            y_window = series[t:t+out_horizon]                # (out_horizon,)

            X_list.append(x_window)
            Y_list.append(y_window)

            client_list.append(col)
            time_list.append(index[t])  # time of the FIRST predicted hour

    X = np.array(X_list)
    Y = np.array(Y_list)

    # Build DataFrame with metadata + features
    feature_cols = [f"step_{i}" for i in range(1, in_window + 1)]
    target_cols  = [f"target_{i}" for i in range(1, out_horizon + 1)]

    df_features = pd.DataFrame(X, columns=feature_cols)
    df_targets  = pd.DataFrame(Y, columns=target_cols)
    df_meta = pd.DataFrame({
        "client_id": client_list,
        "time": time_list,
    })

    df_supervised = pd.concat([df_meta, df_targets, df_features], axis=1)

    return X, Y, df_supervised


# =========================================
# 2. Split clients into train/test
# =========================================

def split_clients(df_hourly, train_ratio=0.8, seed=123):
    """
    Randomly splits clients into train/test sets based on a ratio.

    Args:
        df_hourly  : DataFrame (T x N_clients)
        train_ratio: float, fraction of clients for training (0 < r < 1)
        seed       : int, random seed for reproducibility

    Returns:
        df_train_clients : DataFrame with train clients
        df_test_clients  : DataFrame with test clients
        train_clients    : list of client IDs in train
        test_clients     : list of client IDs in test
    """
    all_clients = df_hourly.columns.to_numpy()
    rng = np.random.RandomState(seed)
    rng.shuffle(all_clients)

    n_total = len(all_clients)
    n_train = int(n_total * train_ratio)

    train_clients = all_clients[:n_train]
    test_clients  = all_clients[n_train:]

    df_train_clients = df_hourly[train_clients]
    df_test_clients  = df_hourly[test_clients]

    return df_train_clients, df_test_clients, train_clients, test_clients


# =========================================
# 3. Plot a client's usage
# =========================================

import matplotlib.pyplot as plt

def plot_random_client(df_clients, seed=None, n_hours=24*7, title_prefix=""):
    """
    Plots the time series of a random client (column) from df_clients.

    Args:
        df_clients  : DataFrame with shape (T, N_clients), hourly data.
        seed        : int or None, for reproducible random choice.
        n_hours     : number of hours to plot from the start (use None for all).
        title_prefix: string to prepend to the plot title (e.g., 'Train'/'Test').
    """
    if df_clients is None or df_clients.shape[1] == 0:
        raise ValueError("df_clients must have at least one column (client).")

    rng = np.random.RandomState(seed) if seed is not None else np.random
    client_id = rng.choice(df_clients.columns)

    series = df_clients[client_id]

    if n_hours is not None:
        series = series.iloc[:n_hours]

    plt.figure(figsize=(12, 4))
    plt.plot(series.index, series.values)
    prefix = (title_prefix + " ") if title_prefix else ""
    plt.title(f"{prefix}Client {client_id} — first {len(series)} hours")
    plt.xlabel("Time")
    plt.ylabel("Load (kWh per hour)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(f"Plotted client: {client_id}")


# =========================================
# 4. Put everything together
# =========================================

if __name__ == "__main__":
    file_path = r"C:/Users/PC/Downloads/LD2011_2014.txt"  # adjust path

    # Step 1: hourly conversion
    df_hourly = load_hourly_df(file_path)
    print("Hourly shape:", df_hourly.shape)
    
    df_cleaned, zero_ratio = filter_clients_by_zero_ratio(df_hourly, max_zero_ratio=0.1)
    print("Original clients:", df_hourly.shape[1])
    print("Cleaned clients:", df_cleaned.shape[1])

    # Step 2: random client split (fixed seed)
    df_train_clients, df_test_clients, train_clients, test_clients = split_clients(
        df_cleaned,
        train_ratio=0.8, # 80-20 split between train and test
        seed=123  # DO NOT CHANGE THE VALUE OF THIS SEED FOR REPRODUCIBILITY
    )

    print("Train clients:", len(train_clients))
    print("Test clients:", len(test_clients))
    
    X_train, Y_train, df_train_sup = make_supervised_from_clients_multi(df_train_clients, in_window=48, out_horizon=24)
    X_test,  Y_test,  df_test_sup  = make_supervised_from_clients_multi(df_test_clients,  in_window=48, out_horizon=24)
    
    # Optional for viewing
    plotRandomClient = False
    if plotRandomClient:
        # Random client from training set
        plot_random_client(df_train_clients, n_hours=24*200, title_prefix="Train")
        
        # Random client from test set
        plot_random_client(df_test_clients, n_hours=24*200, title_prefix="Test")


