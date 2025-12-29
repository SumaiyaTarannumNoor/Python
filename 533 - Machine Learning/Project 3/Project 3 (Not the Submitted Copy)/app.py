import os
import numpy as np
import kagglehub
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, mean_squared_error, roc_auc_score
from sklearn.preprocessing import label_binarize


# -----------------------------
# Utility Functions
# -----------------------------
def relu(x):
    return np.maximum(0, x)


def softmax(x):
    exp = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp / np.sum(exp, axis=1, keepdims=True)


def cross_entropy(pred, y):
    n = y.shape[0]
    return -np.sum(np.log(pred[np.arange(n), y] + 1e-9)) / n


# -----------------------------
# Layers
# -----------------------------
class Conv2D:
    def __init__(self, in_channels, out_channels, kernel_size):
        self.k = kernel_size
        self.W = np.random.randn(out_channels, in_channels, kernel_size, kernel_size).astype(np.float32) * 0.1
        self.b = np.zeros(out_channels, dtype=np.float32)

    def forward(self, x):
        n, c, h, w = x.shape
        out_h = h - self.k + 1
        out_w = w - self.k + 1
        out = np.zeros((n, self.W.shape[0], out_h, out_w), dtype=np.float32)

        for i in range(out_h):
            for j in range(out_w):
                region = x[:, :, i:i+self.k, j:j+self.k]
                out[:, :, i, j] = np.tensordot(
                    region, self.W, axes=([1, 2, 3], [1, 2, 3])
                ) + self.b
        return out


class MaxPool2D:
    def forward(self, x):
        n, c, h, w = x.shape
        out = np.zeros((n, c, h // 2, w // 2), dtype=np.float32)
        for i in range(0, h, 2):
            for j in range(0, w, 2):
                out[:, :, i//2, j//2] = np.max(
                    x[:, :, i:i+2, j:j+2], axis=(2, 3)
                )
        return out


class Linear:
    def __init__(self, in_features, out_features):
        self.W = np.random.randn(in_features, out_features).astype(np.float32) * 0.01
        self.b = np.zeros(out_features, dtype=np.float32)

    def forward(self, x):
        self.x = x
        return x @ self.W + self.b

    def backward(self, dout, lr):
        dW = self.x.T @ dout
        db = np.sum(dout, axis=0)
        self.W -= lr * dW
        self.b -= lr * db


# -----------------------------
# CNN Model
# -----------------------------
class SimpleCNN:
    def __init__(self):
        self.conv = Conv2D(1, 4, 3)   # reduced filters (memory safe)
        self.pool = MaxPool2D()
        self.fc = Linear(4 * 13 * 13, 10)

    def forward(self, x):
        x = self.conv.forward(x)
        x = relu(x)
        x = self.pool.forward(x)
        x = x.reshape(x.shape[0], -1)
        return self.fc.forward(x)


# -----------------------------
# Data Loader
# -----------------------------
def load_csv(path):
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    y = data[:, 0].astype(int)
    x = data[:, 1:].reshape(-1, 1, 28, 28).astype(np.float32) / 255.0
    return x, y


def train_val_split(x, y, val_ratio=0.1):
    idx = np.random.permutation(len(x))
    val_size = int(len(x) * val_ratio)
    return (
        x[idx[val_size:]], y[idx[val_size:]],
        x[idx[:val_size]], y[idx[:val_size]]
    )


# -----------------------------
# Batch Evaluation (SAFE)
# -----------------------------
def evaluate_epoch(model, x, y, batch_size=128):
    losses = []
    preds = []

    for i in range(0, len(x), batch_size):
        xb = x[i:i+batch_size]
        yb = y[i:i+batch_size]

        logits = model.forward(xb)
        probs = softmax(logits)

        losses.append(cross_entropy(probs, yb))
        preds.append(np.argmax(probs, axis=1))

    preds = np.concatenate(preds)
    return np.mean(losses), accuracy_score(y, preds)


# -----------------------------
# Training
# -----------------------------
def train(model, x_train, y_train, x_val, y_val,
          epochs=100, lr=0.01, batch_size=64):

    train_losses, val_losses = [], []
    train_accs, val_accs = [], []

    for epoch in range(epochs):
        idx = np.random.permutation(len(x_train))
        x_train, y_train = x_train[idx], y_train[idx]

        for i in range(0, len(x_train), batch_size):
            xb = x_train[i:i+batch_size]
            yb = y_train[i:i+batch_size]

            logits = model.forward(xb)
            probs = softmax(logits)

            grad = probs
            grad[np.arange(len(yb)), yb] -= 1
            grad /= len(yb)

            model.fc.backward(grad, lr)

        tr_loss, tr_acc = evaluate_epoch(model, x_train, y_train)
        val_loss, val_acc = evaluate_epoch(model, x_val, y_val)

        train_losses.append(tr_loss)
        val_losses.append(val_loss)
        train_accs.append(tr_acc)
        val_accs.append(val_acc)

        print(
            f"Epoch {epoch+1:02d} | "
            f"Train Loss: {tr_loss:.4f} | "
            f"Train Acc: {tr_acc:.4f} | "
            f"Val Acc: {val_acc:.4f}"
        )

    return train_losses, val_losses, train_accs, val_accs


# -----------------------------
# Final Evaluation
# -----------------------------
def evaluate(model, x, y):
    logits = model.forward(x)
    probs = softmax(logits)
    preds = np.argmax(probs, axis=1)

    acc = accuracy_score(y, preds)
    mse = mean_squared_error(y, preds)
    auc = roc_auc_score(
        label_binarize(y, classes=list(range(10))),
        probs,
        multi_class="ovr"
    )
    return acc, mse, auc


# -----------------------------
# Plotting
# -----------------------------
def save_plots(train_losses, val_losses, train_accs, val_accs):
    os.makedirs("results", exist_ok=True)

    plt.figure()
    plt.plot(train_losses, label="Train Loss")
    plt.plot(val_losses, label="Val Loss")
    plt.legend()
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Loss Curve")
    plt.savefig("results/loss_curve.png")
    plt.close()

    plt.figure()
    plt.plot(train_accs, label="Train Accuracy")
    plt.plot(val_accs, label="Val Accuracy")
    plt.legend()
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Accuracy Curve")
    plt.savefig("results/accuracy_curve.png")
    plt.close()


# -----------------------------
# Main (REQUIRED)
# -----------------------------
def main():
    dataset_path = kagglehub.dataset_download("zalando-research/fashionmnist")

    x_full, y_full = load_csv(
        os.path.join(dataset_path, "fashion-mnist_train.csv")
    )
    x_test, y_test = load_csv(
        os.path.join(dataset_path, "fashion-mnist_test.csv")
    )

    x_train, y_train, x_val, y_val = train_val_split(x_full, y_full)

    model = SimpleCNN()

    train_losses, val_losses, train_accs, val_accs = train(
        model, x_train, y_train, x_val, y_val
    )

    save_plots(train_losses, val_losses, train_accs, val_accs)

    acc, mse, auc = evaluate(model, x_test, y_test)

    print("\nFinal Test Evaluation")
    print(f"Accuracy : {acc:.4f}")
    print(f"MSE      : {mse:.4f}")
    print(f"AUC      : {auc:.4f}")


if __name__ == "__main__":
    main()
