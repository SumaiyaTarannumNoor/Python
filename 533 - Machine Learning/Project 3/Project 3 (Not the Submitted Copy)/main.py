import os
import numpy as np
import kagglehub
from sklearn.metrics import accuracy_score, mean_squared_error, roc_auc_score
from sklearn.preprocessing import label_binarize


# -----------------------------
# Utility Functions
# -----------------------------
def relu(x):
    return np.maximum(0, x)


def relu_backward(dout, x):
    dx = dout.copy()
    dx[x <= 0] = 0
    return dx


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
        self.W = np.random.randn(out_channels, in_channels, kernel_size, kernel_size) * 0.1
        self.b = np.zeros(out_channels)

    def forward(self, x):
        self.x = x
        n, c, h, w = x.shape
        out_h = h - self.k + 1
        out_w = w - self.k + 1
        out = np.zeros((n, self.W.shape[0], out_h, out_w))

        for i in range(out_h):
            for j in range(out_w):
                region = x[:, :, i:i+self.k, j:j+self.k]
                out[:, :, i, j] = np.tensordot(region, self.W, axes=([1,2,3],[1,2,3])) + self.b

        return out


class MaxPool2D:
    def __init__(self, size):
        self.size = size

    def forward(self, x):
        self.x = x
        n, c, h, w = x.shape
        out = np.zeros((n, c, h//2, w//2))

        for i in range(0, h, 2):
            for j in range(0, w, 2):
                out[:, :, i//2, j//2] = np.max(x[:, :, i:i+2, j:j+2], axis=(2,3))

        return out


class Linear:
    def __init__(self, in_features, out_features):
        self.W = np.random.randn(in_features, out_features) * 0.01
        self.b = np.zeros(out_features)

    def forward(self, x):
        self.x = x
        return x @ self.W + self.b

    def backward(self, dout, lr):
        dW = self.x.T @ dout
        db = np.sum(dout, axis=0)
        dx = dout @ self.W.T

        self.W -= lr * dW
        self.b -= lr * db
        return dx


# -----------------------------
# CNN Model
# -----------------------------
class SimpleCNN:
    def __init__(self):
        self.conv = Conv2D(1, 8, 3)
        self.pool = MaxPool2D(2)
        self.fc = Linear(8 * 13 * 13, 10)

    def forward(self, x):
        x = self.conv.forward(x)
        self.relu_x = x
        x = relu(x)
        x = self.pool.forward(x)
        self.flat = x.reshape(x.shape[0], -1)
        return self.fc.forward(self.flat)


# -----------------------------
# Data Loader
# -----------------------------
def load_csv(path):
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    y = data[:, 0].astype(int)
    x = data[:, 1:].reshape(-1, 1, 28, 28) / 255.0
    return x, y


# -----------------------------
# Training
# -----------------------------
def train(model, x, y, epochs=3, lr=0.01, batch_size=64):
    for epoch in range(epochs):
        idx = np.random.permutation(len(x))
        x, y = x[idx], y[idx]

        for i in range(0, len(x), batch_size):
            xb = x[i:i+batch_size]
            yb = y[i:i+batch_size]

            logits = model.forward(xb)
            probs = softmax(logits)
            loss = cross_entropy(probs, yb)

            grad = probs
            grad[np.arange(len(yb)), yb] -= 1
            grad /= len(yb)

            model.fc.backward(grad, lr)

        print(f"Epoch {epoch+1} | Loss: {loss:.4f}")


# -----------------------------
# Evaluation
# -----------------------------
def evaluate(model, x, y):
    logits = model.forward(x)
    probs = softmax(logits)
    preds = np.argmax(probs, axis=1)

    acc = accuracy_score(y, preds)
    mse = mean_squared_error(y, preds)

    y_bin = label_binarize(y, classes=list(range(10)))
    auc = roc_auc_score(y_bin, probs, multi_class="ovr")

    return acc, mse, auc


# -----------------------------
# Main (REQUIRED)
# -----------------------------
def main():
    dataset_path = kagglehub.dataset_download("zalando-research/fashionmnist")

    train_x, train_y = load_csv(os.path.join(dataset_path, "fashion-mnist_train.csv"))
    test_x, test_y = load_csv(os.path.join(dataset_path, "fashion-mnist_test.csv"))

    model = SimpleCNN()
    train(model, train_x, train_y)

    acc, mse, auc = evaluate(model, test_x, test_y)

    print("\nFinal Evaluation")
    print(f"Accuracy : {acc:.4f}")
    print(f"MSE      : {mse:.4f}")
    print(f"AUC      : {auc:.4f}")


if __name__ == "__main__":
    main()
