# This example implements the simple neural network on the iris dataset

import numpy as np
from sklearn import datasets

from nnet.models import NeuralNet
from nnet.layers import Dense, Dropout

# Main function
def main():
    # Training parameters
    LEARNING_RATE = 0.005
    MAX_EPOCHS = 70
    BATCHSIZE = 5
    VALIDATION_RATE = 0.04

    # Define neural network architecture
    net = NeuralNet(lr=LEARNING_RATE, optimizer='Adam')
    net.add_layer(Dense(n_in=4, n_out=64, activation='sigmoid'))
    net.add_layer(Dropout(n_in=64, rate=0.4))
    net.add_layer(Dense(n_in=64, n_out=16, activation='sigmoid'))
    net.add_layer(Dropout(n_in=16, rate=0.2))
    net.add_layer(Dense(n_in=16, n_out=3, activation='softmax'))

    # Parse data
    parser = IrisParser()
    iris = datasets.load_iris()
    Y = parser.parseY(iris.target)
    X = parser.parseX(iris.data)

    # Shuffle data to prevent biased validation/test set splits
    n_features = X.shape[1]
    XY = np.concatenate([X, Y], axis=1)
    np.random.shuffle(XY)    
    X = XY[:,0:n_features]
    Y = XY[:,n_features:]

    # Split data
    X_train = X[0:135,:]
    Y_train = Y[0:135,:]
    X_test = X[135:,:]
    Y_test = Y[135:,:]

    # Check accuracy of initial model with test set
    Y_pred = net.predict(X_test)
    comp = (np.argmax(Y_test, axis=1) == np.argmax(Y_pred, axis=1))
    acc = np.sum(comp) / comp.size
    print('Test accuracy before training:', acc*100, '%')

    # Train
    net.train(X_train, Y_train, 
            max_epochs = MAX_EPOCHS, 
            batchsize = BATCHSIZE,
            validation_rate = VALIDATION_RATE, 
            early_stop=False,
            verbose=True)

    # Check final accuracy with test set
    Y_pred = net.predict(X_test)
    comp = (np.argmax(Y_test, axis=1) == np.argmax(Y_pred, axis=1))
    acc = np.sum(comp) / comp.size
    print('Test accuracy after training:', acc*100, '%')

# Parser for the Iris dataset
class IrisParser:
    # Data parser
    def parseX(self, data):
        # Update normalization parameters
        self.mu_x = np.mean(data, axis=0)
        self.sigma_x = np.std(data, axis=0)

        # Normalize
        X = self.normalize(data)

        return X

    # Label parser
    def parseY(self, target):
        Y = np.zeros([len(target), np.max(target)+1])
        for i in range(len(target)):
            Y[i, target[i]] = 1
        return Y

    # Normalize data
    def normalize(self, data):
        X = (data - self.mu_x) / self.sigma_x
        return X


if __name__ == '__main__':
    main()
