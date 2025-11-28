import numpy as np
import pandas as pd
import pickle
import sys
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc
)

# ========================
# MLP Model Implementation
# ========================

class MLP:
    def __init__(self, layer_sizes, activations=None, seed=42, dropout_rates=None):
        np.random.seed(seed)
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes) - 1

        self.activations = ['relu'] * (self.num_layers - 1) if activations is None else activations
        self.dropout_rates = [0.0] * (self.num_layers - 1) if dropout_rates is None else dropout_rates

        self.params = {}
        for i in range(self.num_layers):
            input_size = layer_sizes[i]
            output_size = layer_sizes[i + 1]
            limit = np.sqrt(6.0 / (input_size + output_size))
            self.params['W' + str(i)] = np.random.uniform(-limit, limit, (input_size, output_size))
            self.params['b' + str(i)] = np.zeros(output_size)

        self.m = {}
        self.v = {}
        for key in self.params:
            self.m[key] = np.zeros_like(self.params[key])
            self.v[key] = np.zeros_like(self.params[key])
        self.t = 0

    def relu(self, z):
        return np.maximum(0, z)
    
    def relu_derivative(self, z):
        return (z > 0).astype(float)
    
    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
    
    def forward(self, X, training=True):
        cache = {}
        cache['A0'] = X
        A = X
        for i in range(self.num_layers):
            W = self.params['W' + str(i)]
            b = self.params['b' + str(i)]
            Z = np.dot(A, W) + b
            cache['Z' + str(i)] = Z
            if i == self.num_layers - 1:
                A = self.sigmoid(Z)
            else:
                A = self.relu(Z)
                if training and self.dropout_rates[i] > 0:
                    mask = np.random.rand(*A.shape) > self.dropout_rates[i]
                    A = A * mask / (1.0 - self.dropout_rates[i])
                    cache['dropout_mask' + str(i)] = mask
            cache['A' + str(i + 1)] = A
        return A, cache
    
    def backward(self, y_pred, y_true, cache, class_weights=None):
        m = y_true.shape[0]
        grads = {}
        if class_weights is not None:
            sample_weights = np.array([class_weights[int(y)] for y in y_true]).reshape(-1, 1)
            dA = (y_pred.reshape(-1, 1) - y_true.reshape(-1, 1)) * sample_weights / m
        else:
            dA = (y_pred.reshape(-1, 1) - y_true.reshape(-1, 1)) / m
        for i in range(self.num_layers - 1, -1, -1):
            A_prev = cache['A' + str(i)]
            grads['W' + str(i)] = np.dot(A_prev.T, dA)
            grads['b' + str(i)] = np.sum(dA, axis=0)
            if i > 0:
                W = self.params['W' + str(i)]
                dA = np.dot(dA, W.T)
                Z_prev = cache['Z' + str(i - 1)]
                dA = dA * self.relu_derivative(Z_prev)
                if 'dropout_mask' + str(i - 1) in cache:
                    mask = cache['dropout_mask' + str(i - 1)]
                    dA = dA * mask / (1.0 - self.dropout_rates[i - 1])
        return grads

    def update_params(self, grads, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.t += 1
        for key in self.params:
            self.m[key] = beta1 * self.m[key] + (1 - beta1) * grads[key]
            self.v[key] = beta2 * self.v[key] + (1 - beta2) * (grads[key] ** 2)
            m_hat = self.m[key] / (1 - beta1 ** self.t)
            v_hat = self.v[key] / (1 - beta2 ** self.t)
            self.params[key] -= learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)

    def save_model(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.params, f)
    
    def load_model(self, filepath):
        with open(filepath, 'rb') as f:
            self.params = pickle.load(f)


# ========================
# Data Preprocessing Utils
# ========================

class SimpleScaler:
    def __init__(self):
        self.mean = None
        self.std = None
    
    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        self.std[self.std == 0] = 1.0
    
    def transform(self, X):
        return (X - self.mean) / self.std
    
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

def load_and_preprocess(csv_path, target_col='LUNG_CANCER', scaler=None):
    df = pd.read_csv(csv_path)
    df.columns = [col.strip() for col in df.columns]
    if df[target_col].dtype == 'object':
        df[target_col] = df[target_col].apply(lambda x: 1 if str(x).upper() == 'YES' else 0)
    y = df[target_col].values
    X = df.drop(columns=[target_col])
    X = pd.get_dummies(X, drop_first=True)
    X = X.fillna(X.median())
    X = X.values.astype(float)
    if scaler is None:
        scaler = SimpleScaler()
        X = scaler.fit_transform(X)
    else:
        X = scaler.transform(X)
    return X, y, scaler

def get_batches(X, y, batch_size=32, shuffle=True):
    n_samples = X.shape[0]
    indices = np.arange(n_samples)
    if shuffle:
        np.random.shuffle(indices)
    for start_idx in range(0, n_samples, batch_size):
        end_idx = min(start_idx + batch_size, n_samples)
        batch_indices = indices[start_idx:end_idx]
        yield X[batch_indices], y[batch_indices]

def binary_crossentropy_loss(y_pred, y_true):
    y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
    loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return loss

def calculate_class_weights(y):
    classes, counts = np.unique(y, return_counts=True)
    total = len(y)
    weights = {}
    for cls, count in zip(classes, counts):
        weights[int(cls)] = total / (len(classes) * count)
    return weights

def compute_metrics(model, X, y, threshold=0.5):
    predictions, _ = model.forward(X, training=False)
    y_prob = predictions.flatten()
    y_pred = (y_prob >= threshold).astype(int)
    acc = accuracy_score(y, y_pred)
    prec = precision_score(y, y_pred, zero_division=0)
    rec = recall_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)
    cm = confusion_matrix(y, y_pred)
    fpr, tpr, _ = roc_curve(y, y_prob)
    roc_auc = auc(fpr, tpr)
    results = {
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1_score': f1,
        'auc': roc_auc,
        'confusion_matrix': cm,
        'y_prob': y_prob,
        'y_pred': y_pred,
        'fpr': fpr,
        'tpr': tpr
    }
    return results

def print_evaluation_results(results):
    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(f"Accuracy:  {results['accuracy']:.4f}")
    print(f"Precision: {results['precision']:.4f}")
    print(f"Recall:    {results['recall']:.4f}")
    print(f"F1 Score:  {results['f1_score']:.4f}")
    print(f"AUC:       {results['auc']:.4f}")
    print("\nConfusion Matrix:")
    print(results['confusion_matrix'])
    print("="*50 + "\n")

def save_roc_curve(fpr, tpr, roc_auc, filename='roc_curve.png'):
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"ROC curve saved to {filename}")

def save_confusion_matrix(cm, filename='confusion_matrix.png'):
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=['Negative', 'Positive'],
           yticklabels=['Negative', 'Positive'],
           title='Confusion Matrix',
           ylabel='True label',
           xlabel='Predicted label')
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix saved to {filename}")

# =================
# Data Splitting
# =================

def split_data(input_csv):
    df = pd.read_csv(input_csv)
    print(f"Total samples: {len(df)}")
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        stratify=df['LUNG_CANCER'],
        random_state=42
    )
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        stratify=temp_df['LUNG_CANCER'],
        random_state=42
    )
    train_df.to_csv('train.csv', index=False)
    val_df.to_csv('val.csv', index=False)
    test_df.to_csv('test.csv', index=False)
    print(f"\nSplit completed:")
    print(f"  train.csv: {len(train_df)} samples")
    print(f"  val.csv: {len(val_df)} samples")
    print(f"  test.csv: {len(test_df)} samples")
    print(f"\nFiles saved successfully!")

# =================
# Training Routine
# =================

def train_model(model, X_train, y_train, X_val, y_val, 
                epochs=100, batch_size=32, learning_rate=0.001, 
                class_weights=None):
    print("\nStarting training...")
    train_losses = []
    val_losses = []
    for epoch in range(epochs):
        epoch_losses = []
        for X_batch, y_batch in get_batches(X_train, y_train, batch_size, shuffle=True):
            y_pred, cache = model.forward(X_batch, training=True)
            y_pred_flat = y_pred.flatten()
            loss = binary_crossentropy_loss(y_pred_flat, y_batch)
            epoch_losses.append(loss)
            grads = model.backward(y_pred, y_batch, cache, class_weights)
            model.update_params(grads, learning_rate)
        avg_train_loss = np.mean(epoch_losses)
        train_losses.append(avg_train_loss)
        val_pred, _ = model.forward(X_val, training=False)
        val_loss = binary_crossentropy_loss(val_pred.flatten(), y_val)
        val_losses.append(val_loss)
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {avg_train_loss:.4f}, Val Loss: {val_loss:.4f}")
    print("Training completed!\n")
    return train_losses, val_losses

def main(train_csv, test_csv):
    print("="*60)
    print("MLP LUNG CANCER PREDICTION")
    print("="*60)
    print("\nLoading training data...")
    X_train, y_train, scaler = load_and_preprocess(train_csv, target_col='LUNG_CANCER')
    print("Loading test data...")
    X_test, y_test, _ = load_and_preprocess(test_csv, target_col='LUNG_CANCER', scaler=scaler)
    print(f"\nDataset Info:")
    print(f"  Training samples: {X_train.shape[0]}")
    print(f"  Test samples: {X_test.shape[0]}")
    print(f"  Number of features: {X_train.shape[1]}")
    print(f"\nClass distribution in training set:")
    unique, counts = np.unique(y_train, return_counts=True)
    for cls, count in zip(unique, counts):
        print(f"  Class {cls}: {count} samples ({count/len(y_train)*100:.1f}%)")
    class_weights = calculate_class_weights(y_train)
    print(f"\nClass weights: {class_weights}")
    input_dim = X_train.shape[1]
    hidden_dim1 = 128
    hidden_dim2 = 64
    output_dim = 1
    layer_sizes = [input_dim, hidden_dim1, hidden_dim2, output_dim]
    activations = ['relu', 'relu']
    dropout_rates = [0.2, 0.1]
    print(f"\nModel Architecture:")
    print(f"  Input layer: {input_dim} neurons")
    print(f"  Hidden layer 1: {hidden_dim1} neurons (ReLU, Dropout=0.2)")
    print(f"  Hidden layer 2: {hidden_dim2} neurons (ReLU, Dropout=0.1)")
    print(f"  Output layer: {output_dim} neuron (Sigmoid)")
    model = MLP(layer_sizes=layer_sizes, activations=activations, dropout_rates=dropout_rates, seed=42)
    model_path = 'final_model.pkl'
    if os.path.exists(model_path):
        print(f"\nFound existing model at {model_path}")
        print("Loading trained model...")
        model.load_model(model_path)
    else:
        print("\nNo existing model found. Training new model...")
        epochs = 100
        batch_size = 32
        learning_rate = 0.001
        train_losses, val_losses = train_model(
            model, X_train, y_train, X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            class_weights=class_weights
        )
        print(f"Saving model to {model_path}...")
        model.save_model(model_path)
    print("\nEvaluating model on test set...")
    results = compute_metrics(model, X_test, y_test, threshold=0.5)
    print_evaluation_results(results)
    print("Generating and saving plots...")
    save_roc_curve(results['fpr'], results['tpr'], results['auc'], 'test_roc_curve.png')
    save_confusion_matrix(results['confusion_matrix'], 'test_confusion_matrix.png')
    print("\nAll done! Check the generated plots.")
    return results

if __name__ == "__main__":
    # If you want to run splitting, uncomment -> split_data('survey lung cancer.csv')
    # split_data('survey lung cancer.csv')
    if len(sys.argv) == 3:
        train_csv_path = sys.argv[1]
        test_csv_path = sys.argv[2]
    else:
        train_csv_path = 'train.csv'
        test_csv_path = 'test.csv'
        print(f"Usage: python lung_cancer_mlp.py <train_csv> <test_csv>")
        print(f"Using default files: {train_csv_path}, {test_csv_path}\n")
    main(train_csv_path, test_csv_path)