import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation, Input
from keras.models import Model
from keras.utils import np_utils


class Stock_Model(object):

    def __init__(self, input_shape=None, time_steps=None, nb_class=None, rolling=False):
        '''
        param: input_shape: the shape of one input sequence
        param: time_steps: the number of sequence in each input
        param: nb_class: the number of target class
        param: rooling: whether to rolling the data
        '''
        if(input_shape == None):
            raise ValueError('input_shape could not be None')
        if(time_steps == None):
            raise ValueError('time_steps could not be None')
        if(nb_class == None):
            raise ValueError('nb_class could not be None')

        self.input_shape = input_shape
        self.nb_class = nb_class
        self.time_steps = time_steps
        self.rolling = rolling

    def train(self, X_train=None, y_train=None, X_test=None, y_test=None):
        # check out the train set
        if(isinstance(X_train, str) and isinstance(y_train, str)):
            X_train = np.loadtxt(X_train, dtype=np.float32, delimiter=',')
            y_train = np.loadtxt(y_train, dtype=np.int, delimiter=',')
        # X_train = np.mat(X_train)
        y_train = y_train.ravel()

        # check out the test set
        if(isinstance(X_test, str) and isinstance(y_test, str)):
            X_test = np.loadtxt(X_test, dtype=np.float32, delimiter=',')
            y_test = np.loadtxt(y_test, dtype=np.int, delimiter=',')
        # X_test = np.mat(X_test)
        y_test = y_test.ravel()

        from keras.utils import to_categorical
        y_train = to_categorical(y_train, self.nb_class)
        y_test = to_categorical(y_test, self.nb_class)

        # roll the data if necessary
        if self.rolling == True:
            temp = []
            for i in range(X_train.shape[0] - self.time_steps):
                temp.append(X_train[i:i + self.time_steps, :])
            if(y_train.shape[0] != len(temp)):
                raise ValueError('the number of train set label mismatch the number of samples'
                                 ' when rolling, the number of label should be %s, but it is %s'
                                 % (str(len(temp)), str(y_train.shape[0])))
            X_train = np.array(temp)

            temp = []
            for i in range(X_test.shape[0] - self.time_steps):
                temp.append(X_test[i:i + self.time_steps, :])
            if(y_test.shape[0] != len(temp)):
                raise ValueError('the number of test set label mismatch the number of samples'
                                 ' when rolling, the number of label should be %s, but it is %s'
                                 % (str(len(temp)), str(y_test.shape[0])))
            X_test = np.array(temp)
        # train the model
        x = Input(shape=(self.time_steps, self.input_shape))
        y = LSTM(32, name='lstm1', return_sequences=True)(x)
        y = Dropout(.2, name='dropout1')(y)
        y = LSTM(64, name='lstm2')(y)
        y = Dropout(.2, name='dropout2')(y)
        y = Dense(128, activation='relu', name='dense1')(y)
        y = Dense(self.nb_class, activation='relu', name='dense2')(y)
        y = Activation('softmax', name='softmax')(y)

        model = Model(x, y)

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, validation_data=(X_test, y_test),
                  batch_size=1, epochs=1, verbose=1)
        model.save('stock_model.h5')


if __name__ == '__main__':
    model = Stock_Model(input_shape=2, time_steps=5, nb_class=3, rolling=True)
    print(model.nb_class)
    model.train(X_train=np.zeros((10, 2)), y_train=np.zeros((1, 5)),
                X_test=np.zeros((10, 2)), y_test=np.zeros((1, 5)))
