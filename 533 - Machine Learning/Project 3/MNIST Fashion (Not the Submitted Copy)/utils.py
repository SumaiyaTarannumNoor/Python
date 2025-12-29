import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, roc_auc_score

CLASS_NAMES = [
    "T-shirt/top","Trouser","Pullover","Dress","Coat",
    "Sandal","Shirt","Sneaker","Bag","Ankle boot"
]

IMG_ROWS = 28
IMG_COLS = 28
NUM_CLASSES = 10

def load_fashion_mnist(csv_path):
    data = pd.read_csv(csv_path)
    y = np.zeros((len(data), NUM_CLASSES))
    y[np.arange(len(data)), data.iloc[:,0]] = 1
    x = data.iloc[:,1:].values.reshape(-1, IMG_ROWS, IMG_COLS, 1) / 255.0
    return x, y

def evaluate_metrics(y_true, y_pred):
    y_pred_cls = np.argmax(y_pred, axis=1)
    y_true_cls = np.argmax(y_true, axis=1)
    accuracy = np.mean(y_pred_cls == y_true_cls)
    auc = roc_auc_score(y_true, y_pred, multi_class="ovr")
    mse = mean_squared_error(y_true, y_pred)
    return accuracy, auc, mse, y_true_cls, y_pred_cls

def save_confusion_matrix(y_true_cls, y_pred_cls, save_path):
    cm = confusion_matrix(y_true_cls, y_pred_cls)
    plt.figure(figsize=(10,8))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def save_accuracy_loss_curve(history, save_path):
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.plot(history['accuracy'], label="Train Accuracy")
    plt.plot(history['val_accuracy'], label="Val Accuracy")
    plt.xlabel("Epoch"); plt.ylabel("Accuracy"); plt.legend()
    plt.subplot(1,2,2)
    plt.plot(history['loss'], label="Train Loss")
    plt.plot(history['val_loss'], label="Val Loss")
    plt.xlabel("Epoch"); plt.ylabel("Loss"); plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def print_classification_report_named(y_true_cls, y_pred_cls):
    print(classification_report(y_true_cls, y_pred_cls, target_names=CLASS_NAMES))
