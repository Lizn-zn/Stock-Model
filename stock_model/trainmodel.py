# _*_ coding:utf-8 _*_
import os
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation, Input
from keras.models import Model, load_model
from keras.utils import np_utils

from matplotlib import pyplot
from sklearn.externals import joblib


class Stock_Model(object):

    def __init__(self, input_dim=None,  nb_class=None):
        '''
        param: input_dim: the shape of one input sequence
        param: time_steps: the number of sequence in each input
        param: nb_class: the number of target class
        param: rooling: whether to rolling the data
        '''
        if(nb_class == None):
            raise ValueError('nb_class could not be None')

        self.input_dim = input_dim
        self.nb_class = nb_class
        self.model = None

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

        if(self.input_dim == None):
            self.input_dim = (X_train.shape[1], X_train.
                              shape[2])

        from keras.utils import to_categorical
        y_train = to_categorical(y_train, self.nb_class)
        y_test = to_categorical(y_test, self.nb_class)

        # train the model
        x = Input(shape=self.input_dim)
        y = LSTM(256, name='lstm1', return_sequences=True)(x)
        y = Dropout(.2, name='dropout1')(y)
        y = LSTM(512, name='lstm2', return_sequences=True)(y)
        y = Dropout(.2, name='dropout2')(y)
        y = LSTM(256, name='lstm3')(y)
        y = Dense(256, activation='tanh', name='dense1')(y)
        y = Dropout(.2, name='dropout3')(y)
        y = Dense(128, activation='tanh', name='dense2')(y)
        y = Dense(256, activation='tanh', name='dense3')(y)
        y = Dense(512, activation='tanh', name='dense4')(y)
        y = Dense(256, activation='tanh', name='dense5')(y)
        y = Dense(128, activation='tanh', name='dense6')(y)
        y = Dense(self.nb_class, activation='sigmoid', name='dense7')(y)
        y = Activation('softmax', name='softmax')(y)

        model = Model(x, y)

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        from keras.callbacks import EarlyStopping
        early_stop = EarlyStopping(
            monitor='val_loss', patience=1, verbose=0, mode='auto')
        model.fit(X_train, y_train, validation_data=[X_test, y_test],
                  batch_size=1280, epochs=30, verbose=1, callbacks=[early_stop])
        self.model = model
        model.save('stock_model.h5')

    def plot_curve(self):
        model = self.model
        pyplot.plot(model.history.history['loss'])
        pyplot.plot(model.history.history['val_loss'])
        pyplot.title('model train & validation loss')
        pyplot.ylabel('loss')
        pyplot.xlabel('epoch')
        pyplot.show()


def roll_data(data, label, time_steps):
    label = label.ravel()
    temp = []
    for i in range(data.shape[0] - time_steps):
        temp.append(data[i:i + time_steps, :])
    if(label.shape[0] != len(temp)):
        raise ValueError('the number of train set label mismatch the number of samples'
                         ' when rolling, the number of label should be %s, but it is %s'
                         % (str(len(temp)), str(label.shape[0])))
    data = np.array(temp)
    return data


def loadData(X_directory, y_directory, time_steps=5):
    if(not os.path.exists('X_data.pkl') or not os.path.exists('y_data.pkl')):
        X_data = []
        y_data = []

        # chech out the path
        if not os.path.exists(X_directory) or not os.path.exists(y_directory):
            raise ValueError('cannot found the data !')

        label = pd.read_csv(y_directory, index_col=0)

        # Get table names
        excel_list = os.listdir(X_directory)

        for excel in excel_list:
            print(excel)

            # Continue if it is not a table
            if not excel.endswith(".csv"):
                continue

            if excel.startswith("~$"):
                continue
            # data = np.loadtxt(directory + '\\' + excel, skiprows=1,
            #                   dtype=str, delimiter=',')
            data = pd.read_csv(X_directory + "\\" + excel, header=1)
            data.fillna(0, inplace=True)
            data = data.iloc[:, 1:].as_matrix().astype(np.float32)

            k = data.shape[0]

            if(k <= time_steps):
                temp_label = np.array([])
                continue
            else:
                temp_label = label.ix[
                    excel[:-4]].as_matrix()[-k + time_steps:].astype(np.int)

            if(temp_label[0] < 0):
                index = np.where(temp_label > 0)[0]
                if(index.shape[0] == 0):
                    continue
                index = index[0]
                data = data[index:, :]
                temp_label = temp_label[index:]

            temp_label -= 1

            data = roll_data(data, temp_label, time_steps)

            if(X_data == []):
                X_data = np.array(data)
            else:
                X_data = np.concatenate((X_data, data), axis=0)
            if(y_data == []):
                y_data = np.array(temp_label)
            else:
                y_data = np.concatenate((y_data, temp_label), axis=0)

        joblib.dump(X_data, 'X_data.pkl')
        joblib.dump(y_data, 'y_data.pkl')
    else:
        X_data = joblib.load('X_data.pkl')
        y_data = joblib.load('y_data.pkl')

    return X_data, y_data


if __name__ == '__main__':
    X_data, y_data = loadData(
        'data\\stock_data_normal', 'data\\label_data\\label.csv')
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X_data, y_data, test_size=0.2, random_state=223)
    model = Stock_Model(input_dim=None, nb_class=3)
    model.train(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
    model.plot_curve()
