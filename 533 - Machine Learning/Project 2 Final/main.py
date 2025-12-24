# import os
# import argparse
# import random
# import numpy as np
# import matplotlib.pyplot as plt
# from dataclasses import dataclass

# from load_time_series_dataset import (
#     load_hourly_df,
#     filter_clients_by_zero_ratio,
#     split_clients,
#     make_supervised_from_clients_multi,
# )

# # -----------------------------
# # Reproducibility
# # -----------------------------
# def set_seed(seed=123):
#     random.seed(seed)
#     np.random.seed(seed)


# # -----------------------------
# # Normalization
# # -----------------------------
# @dataclass
# class Standardizer:
#     mean: float
#     std: float

#     def transform(self, x):
#         return (x - self.mean) / (self.std + 1e-8)

#     def inverse_transform(self, x):
#         return x * (self.std + 1e-8) + self.mean


# def fit_standardizer(x, y):
#     flat = np.concatenate([x.reshape(-1), y.reshape(-1)])
#     return Standardizer(np.mean(flat), np.std(flat) + 1e-8)


# # -----------------------------
# # Metrics
# # -----------------------------
# def mse(y_true, y_pred):
#     return np.mean((y_true - y_pred) ** 2)


# def accuracy_from_mse(mse_val, var):
#     return max(0.0, 100.0 * (1.0 - mse_val / var))


# # -----------------------------
# # Linear Forecast Model (RAW PYTHON)
# # -----------------------------
# class LinearForecaster:
#     def __init__(self, in_dim=48, out_dim=24):
#         self.W = np.random.randn(in_dim, out_dim) * 0.01
#         self.b = np.zeros(out_dim)

#     def predict(self, X):
#         return X @ self.W + self.b

#     def train_step(self, X, Y, lr):
#         preds = self.predict(X)
#         error = preds - Y

#         grad_W = X.T @ error / len(X)
#         grad_b = np.mean(error, axis=0)

#         self.W -= lr * grad_W
#         self.b -= lr * grad_b

#         return mse(Y, preds)


# # -----------------------------
# # Training Loop
# # -----------------------------
# def train_one_run(
#     model,
#     X_train,
#     Y_train,
#     X_val,
#     Y_val,
#     lr,
#     epochs,
#     patience,
#     y_var,
#     ckpt_path,
# ):
#     history = {
#         "train_mse": [],
#         "val_mse": [],
#         "val_accuracy": [],
#     }

#     best_acc = -1
#     best_epoch = -1
#     patience_left = patience

#     for epoch in range(1, epochs + 1):
#         train_mse = model.train_step(X_train, Y_train, lr)
#         val_preds = model.predict(X_val)
#         val_mse = mse(Y_val, val_preds)
#         val_acc = accuracy_from_mse(val_mse, y_var)

#         history["train_mse"].append(train_mse)
#         history["val_mse"].append(val_mse)
#         history["val_accuracy"].append(val_acc)

#         if val_acc > best_acc:
#             best_acc = val_acc
#             best_epoch = epoch
#             patience_left = patience
#             os.makedirs(os.path.dirname(ckpt_path), exist_ok=True)
#             np.savez(ckpt_path, W=model.W, b=model.b)
#         else:
#             patience_left -= 1

#         print(
#             f"Epoch {epoch:03d} | "
#             f"Train MSE={train_mse:.5f} | "
#             f"Val MSE={val_mse:.5f} | "
#             f"Val Acc={val_acc:.2f}%"
#         )

#         if patience_left <= 0:
#             print("Early stopping triggered")
#             break

#     return history, best_acc, best_epoch


# # -----------------------------
# # Plots
# # -----------------------------
# def plot_training(history, out_path):
#     epochs = range(1, len(history["train_mse"]) + 1)

#     fig, ax1 = plt.subplots(figsize=(10, 4))
#     ax1.plot(epochs, history["train_mse"], label="Train MSE")
#     ax1.plot(epochs, history["val_mse"], label="Val MSE")
#     ax1.set_ylabel("MSE")
#     ax1.grid(True)

#     ax2 = ax1.twinx()
#     ax2.plot(epochs, history["val_accuracy"], "--", label="Val Accuracy")
#     ax2.set_ylabel("Accuracy (%)")

#     lines, labels = ax1.get_legend_handles_labels()
#     lines2, labels2 = ax2.get_legend_handles_labels()
#     ax1.legend(lines + lines2, labels + labels2)

#     plt.tight_layout()
#     plt.savefig(out_path, dpi=150)
#     plt.close()


# def plot_forecast(y_true, y_pred, out_path):
#     plt.figure(figsize=(10, 4))
#     plt.plot(y_true, label="True")
#     plt.plot(y_pred, label="Predicted")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(out_path, dpi=150)
#     plt.close()


# # -----------------------------
# # Main
# # -----------------------------
# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--data_path", default="./LD2011_2014.txt")
#     parser.add_argument("--epochs", type=int, default=80)
#     parser.add_argument("--lr", type=float, default=1e-3)
#     parser.add_argument("--patience", type=int, default=10)
#     args = parser.parse_args()

#     set_seed()

#     # Load dataset
#     df = load_hourly_df(args.data_path)
#     df, _ = filter_clients_by_zero_ratio(df, 0.10)

#     # Split clients into train, validation, test
#     df_train, df_test, _, _ = split_clients(df, 0.8, 123)  # 80% for train+val, 20% test
#     n_train = int(0.9 * len(df_train))  # 90% of train+val for training, 10% for validation
#     df_tr, df_val = df_train[:n_train], df_train[n_train:]

#     # Create supervised datasets
#     X_tr, Y_tr, _ = make_supervised_from_clients_multi(df_tr, 48, 24)
#     X_val, Y_val, _ = make_supervised_from_clients_multi(df_val, 48, 24)
#     X_te, Y_te, _ = make_supervised_from_clients_multi(df_test, 48, 24)

#     # Standardize
#     scaler = fit_standardizer(X_tr, Y_tr)
#     X_tr, Y_tr = scaler.transform(X_tr), scaler.transform(Y_tr)
#     X_val, Y_val = scaler.transform(X_val), scaler.transform(Y_val)
#     X_te, Y_te = scaler.transform(X_te), scaler.transform(Y_te)

#     y_var = np.var(Y_tr)

#     model = LinearForecaster()
#     os.makedirs("results", exist_ok=True)

#     history, best_acc, best_epoch = train_one_run(
#         model,
#         X_tr,
#         Y_tr,
#         X_val,
#         Y_val,
#         args.lr,
#         args.epochs,
#         args.patience,
#         y_var,
#         "results/best_model.npz",
#     )

#     print(f"\nBEST VALIDATION ACCURACY: {best_acc:.2f}% (epoch {best_epoch})")

#     test_preds = model.predict(X_te)
#     test_mse = mse(Y_te, test_preds)
#     test_acc = accuracy_from_mse(test_mse, y_var)
#     print(f"FINAL TEST ACCURACY: {test_acc:.2f}%")

#     plot_training(history, "results/training_curves.png")
#     plot_forecast(Y_te[0], test_preds[0], "results/forecast_example.png")


# if __name__ == "__main__":
#     main()


import os
import argparse
import random
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

from load_time_series_dataset import (
    load_hourly_df,
    filter_clients_by_zero_ratio,
    split_clients,
    make_supervised_from_clients_multi,
)

# -----------------------------
# Reproducibility
# -----------------------------
def set_seed(seed=123):
    random.seed(seed)
    np.random.seed(seed)


# -----------------------------
# Normalization
# -----------------------------
@dataclass
class Standardizer:
    mean: float
    std: float

    def transform(self, x):
        return (x - self.mean) / (self.std + 1e-8)

    def inverse_transform(self, x):
        return x * (self.std + 1e-8) + self.mean


def fit_standardizer(x, y):
    flat = np.concatenate([x.reshape(-1), y.reshape(-1)])
    return Standardizer(np.mean(flat), np.std(flat) + 1e-8)


# -----------------------------
# Metrics
# -----------------------------
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


def accuracy_from_mse(mse_val, var):
    return max(0.0, 100.0 * (1.0 - mse_val / var))


# -----------------------------
# Linear Forecast Model (RAW PYTHON)
# -----------------------------
class LinearForecaster:
    def __init__(self, in_dim=48, out_dim=24):
        self.W = np.random.randn(in_dim, out_dim) * 0.01
        self.b = np.zeros(out_dim)

    def predict(self, X):
        return X @ self.W + self.b

    def train_step(self, X, Y, lr):
        preds = self.predict(X)
        error = preds - Y

        grad_W = X.T @ error / len(X)
        grad_b = np.mean(error, axis=0)

        self.W -= lr * grad_W
        self.b -= lr * grad_b

        return mse(Y, preds)

    def load(self, path):
        ckpt = np.load(path)
        self.W = ckpt["W"]
        self.b = ckpt["b"]


# -----------------------------
# Training Loop
# -----------------------------
def train_one_run(
    model,
    X_train,
    Y_train,
    X_val,
    Y_val,
    lr,
    epochs,
    patience,
    y_var,
    ckpt_path,
):
    history = {
        "train_mse": [],
        "val_mse": [],
        "val_accuracy": [],
    }

    best_acc = -1
    best_epoch = -1
    patience_left = patience

    for epoch in range(1, epochs + 1):
        train_mse = model.train_step(X_train, Y_train, lr)
        val_preds = model.predict(X_val)
        val_mse = mse(Y_val, val_preds)
        val_acc = accuracy_from_mse(val_mse, y_var)

        history["train_mse"].append(train_mse)
        history["val_mse"].append(val_mse)
        history["val_accuracy"].append(val_acc)

        if val_acc > best_acc:
            best_acc = val_acc
            best_epoch = epoch
            patience_left = patience
            os.makedirs(os.path.dirname(ckpt_path), exist_ok=True)
            np.savez(ckpt_path, W=model.W, b=model.b)
        else:
            patience_left -= 1

        print(
            f"Epoch {epoch:03d} | "
            f"Train MSE={train_mse:.5f} | "
            f"Val MSE={val_mse:.5f} | "
            f"Val Acc={val_acc:.2f}%"
        )

        if patience_left <= 0:
            print("Early stopping triggered")
            break

    return history, best_acc, best_epoch


# -----------------------------
# Plots
# -----------------------------
def plot_training(history, out_path):
    epochs = range(1, len(history["train_mse"]) + 1)

    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(epochs, history["train_mse"], label="Train MSE")
    ax1.plot(epochs, history["val_mse"], label="Val MSE")
    ax1.set_ylabel("MSE")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(epochs, history["val_accuracy"], "--", label="Val Accuracy")
    ax2.set_ylabel("Accuracy (%)")

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved training curves → {out_path}")


def plot_forecast(y_true, y_pred, out_path):
    plt.figure(figsize=(10, 4))
    plt.plot(y_true, label="True")
    plt.plot(y_pred, label="Predicted")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved forecast example → {out_path}")


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="./LD2011_2014.txt")
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--patience", type=int, default=10)
    args = parser.parse_args()

    set_seed()

    # Load dataset
    df = load_hourly_df(args.data_path)
    df, _ = filter_clients_by_zero_ratio(df, 0.10)

    # Split clients
    df_train, df_test, _, _ = split_clients(df, 0.8, 123)
    n_train = int(0.9 * len(df_train))
    df_tr, df_val = df_train[:n_train], df_train[n_train:]

    # Supervised data
    X_tr, Y_tr, _ = make_supervised_from_clients_multi(df_tr, 48, 24)
    X_val, Y_val, _ = make_supervised_from_clients_multi(df_val, 48, 24)
    X_te, Y_te, _ = make_supervised_from_clients_multi(df_test, 48, 24)

    # Normalize
    scaler = fit_standardizer(X_tr, Y_tr)
    X_tr, Y_tr = scaler.transform(X_tr), scaler.transform(Y_tr)
    X_val, Y_val = scaler.transform(X_val), scaler.transform(Y_val)
    X_te, Y_te = scaler.transform(X_te), scaler.transform(Y_te)

    y_var = np.var(Y_tr)

    model = LinearForecaster()
    os.makedirs("results", exist_ok=True)

    history, best_acc, best_epoch = train_one_run(
        model,
        X_tr,
        Y_tr,
        X_val,
        Y_val,
        args.lr,
        args.epochs,
        args.patience,
        y_var,
        "results/best_model.npz",
    )

    print(f"\nBEST VALIDATION ACCURACY: {best_acc:.2f}% (epoch {best_epoch})")

    # -------- LOAD BEST MODEL BEFORE TESTING --------
    model.load("results/best_model.npz")

    # -------- FINAL TEST EVALUATION --------
    test_preds = model.predict(X_te)
    test_mse = mse(Y_te, test_preds)
    test_acc = accuracy_from_mse(test_mse, y_var)

    print("\n===== FINAL TEST RESULTS =====")
    print(f"Test MSE      : {test_mse:.6f}")
    print(f"Test Accuracy : {test_acc:.2f}%")
    print(f"Pred shape    : {test_preds.shape}")

    np.save("results/test_predictions.npy", test_preds)
    print("Saved test predictions → results/test_predictions.npy")

    plot_training(history, "results/training_curves.png")
    plot_forecast(Y_te[0], test_preds[0], "results/forecast_example.png")


if __name__ == "__main__":
    main()
