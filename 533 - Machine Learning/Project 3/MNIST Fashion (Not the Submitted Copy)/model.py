# 

import numpy as np

# ------------------------
# Activation Functions
# ------------------------
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def softmax(x):
    exp = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp / np.sum(exp, axis=1, keepdims=True)

# ------------------------
# Loss Function
# ------------------------
def cross_entropy_loss(y_true, y_pred):
    eps = 1e-12
    y_pred = np.clip(y_pred, eps, 1. - eps)
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))

# ------------------------
# Layers
# ------------------------
class Conv2D:
    def __init__(self, num_filters, kernel_size, input_depth):
        self.num_filters = num_filters
        self.kernel_size = kernel_size
        self.input_depth = input_depth
        scale = np.sqrt(2.0 / (kernel_size*kernel_size*input_depth))
        self.weights = np.random.randn(num_filters, kernel_size, kernel_size, input_depth) * scale
        self.bias = np.zeros((num_filters, 1))
        
    def forward(self, x):
        self.x = x
        batch, h, w, c = x.shape
        kh, kw = self.kernel_size, self.kernel_size
        out_h = h - kh + 1
        out_w = w - kw + 1
        self.output = np.zeros((batch, out_h, out_w, self.num_filters))
        for i in range(out_h):
            for j in range(out_w):
                patch = x[:, i:i+kh, j:j+kw, :]
                for f in range(self.num_filters):
                    self.output[:, i, j, f] = np.sum(patch * self.weights[f], axis=(1,2,3))
        self.output += self.bias.T
        return relu(self.output)

class MaxPool2D:
    def __init__(self, pool_size=2):
        self.pool_size = pool_size
    
    def forward(self, x):
        self.x = x
        batch, h, w, c = x.shape
        ph, pw = self.pool_size, self.pool_size
        out_h, out_w = h // ph, w // pw
        self.output = np.zeros((batch, out_h, out_w, c))
        for i in range(out_h):
            for j in range(out_w):
                patch = x[:, i*ph:(i+1)*ph, j*pw:(j+1)*pw, :]
                self.output[:, i, j, :] = np.max(patch, axis=(1,2))
        return self.output

class Flatten:
    def forward(self, x):
        self.input_shape = x.shape
        return x.reshape(x.shape[0], -1)

class Dense:
    def __init__(self, input_size, output_size):
        scale = np.sqrt(2.0 / input_size)
        self.weights = np.random.randn(input_size, output_size) * scale
        self.bias = np.zeros((1, output_size))
    
    def forward(self, x):
        self.x = x
        return relu(np.dot(x, self.weights) + self.bias)
