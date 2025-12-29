import os
import numpy as np
from utils import load_fashion_mnist, evaluate_metrics, save_confusion_matrix, save_accuracy_loss_curve, print_classification_report_named
from model import Dense, softmax, cross_entropy_loss

PATH = "./"
TRAIN_FILE = PATH + "dataset/fashion-mnist_train.csv"
TEST_FILE = PATH + "dataset/fashion-mnist_test.csv"
OUTPUT_DIR = "outputs"

BATCH_SIZE = 64
EPOCHS = 6000
LEARNING_RATE = 0.1

# --------------------------
# Simple Dense-only CNN proxy
# --------------------------
def train_model(X_train, y_train, X_val, y_val):
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_val_flat = X_val.reshape(X_val.shape[0], -1)

    fc = Dense(X_train_flat.shape[1], y_train.shape[1])

    history = {'accuracy': [], 'val_accuracy': [], 'loss': [], 'val_loss': []}

    for epoch in range(EPOCHS):
        # Forward pass
        z = np.dot(X_train_flat, fc.weights) + fc.bias
        y_pred = softmax(z)

        # Loss
        loss = cross_entropy_loss(y_train, y_pred)

        # Backprop only Dense
        dz = (y_pred - y_train) / y_train.shape[0]
        dW = np.dot(X_train_flat.T, dz)
        db = np.sum(dz, axis=0, keepdims=True)
        fc.weights -= LEARNING_RATE * dW
        fc.bias -= LEARNING_RATE * db

        # Accuracy
        y_pred_cls = np.argmax(y_pred, axis=1)
        y_true_cls = np.argmax(y_train, axis=1)
        acc = np.mean(y_pred_cls == y_true_cls)

        # Validation
        z_val = np.dot(X_val_flat, fc.weights) + fc.bias
        y_val_pred = softmax(z_val)
        val_loss = cross_entropy_loss(y_val, y_val_pred)
        val_pred_cls = np.argmax(y_val_pred, axis=1)
        val_true_cls = np.argmax(y_val, axis=1)
        val_acc = np.mean(val_pred_cls == val_true_cls)

        history['accuracy'].append(acc)
        history['val_accuracy'].append(val_acc)
        history['loss'].append(loss)
        history['val_loss'].append(val_loss)

        print(f"Epoch {epoch+1}/{EPOCHS} - loss: {loss:.4f} - acc: {acc:.4f} - val_loss: {val_loss:.4f} - val_acc: {val_acc:.4f}")

    return history, fc

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    X_train, y_train = load_fashion_mnist(TRAIN_FILE)
    X_val, y_val = load_fashion_mnist(TEST_FILE)

    history, model = train_model(X_train, y_train, X_val, y_val)

    # Test evaluation
    X_test_flat = X_val.reshape(X_val.shape[0], -1)
    y_prob = softmax(np.dot(X_test_flat, model.weights) + model.bias)
    accuracy, auc, mse, y_true_cls, y_pred_cls = evaluate_metrics(y_val, y_prob)

    print("\n===== TEST METRICS =====")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"AUC      : {auc:.4f}")
    print(f"MSE      : {mse:.6f}")

    print_classification_report_named(y_true_cls, y_pred_cls)
    save_confusion_matrix(y_true_cls, y_pred_cls, os.path.join(OUTPUT_DIR,"confusion_matrix.png"))
    save_accuracy_loss_curve(history, os.path.join(OUTPUT_DIR,"accuracy_loss_curve.png"))
    print("\nSaved outputs in 'outputs' folder.")

if __name__ == "__main__":
    main()
