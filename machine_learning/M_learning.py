import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, LSTM
from keras.models import Model, load_model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from datetime import datetime
import os

class M_learning(object):
    
    def __init__(self, win_or_not = None, exchange_or_not = None, file_path_csv = ''):
        self.df = pd.read_csv(file_path_csv, on_bad_lines='skip', engine='python')
                    
        pd.set_option('display.max_columns', 35)
        pd.options.display.float_format = '{:,.3f}'.format
        
        self.X = None
        self.y = None
        self.X_train = None 
        self.X_test = None 
        self.y_train = None 
        self.y_test = None
        self.y_preds = None
        
        self.opt = 'Adam'
        self.l_r = '00001'
        self.filename_updated = ''
        
        self.win_or_not = win_or_not
        self.exchange_or_not = exchange_or_not
    
    def pre_processing(self):        
        self.df.loc[self.df['Exchange'] == '[\'t\']', 'Exchange'] = True
        self.df.loc[self.df['Exchange'] == '[\'n\']', 'Exchange'] = False
        
        self.df.loc[self.df['Win'] == True, 'Win'] = True
        self.df.loc[self.df['Win'] == False, 'Win'] = False

        self.df.drop(columns=['Player ID'], axis=1, inplace=True)
        
        # self.df.drop(columns=['Card Before 1', 'Card Before 2'], 
        #             axis=1, inplace=True)
        
        self.df.drop(columns=['Card Exchanged 1', 'Card Exchanged 2', 'Card Exchanged 3'], 
                    axis=1, inplace=True)
        
        # --------------------------------------- EXCHANGE AMOUNT PREDICTION ---------------------------------------
        if self.exchange_or_not == True:
            self.df = self.df.loc[self.df['Win'] == True]
            print("Length of column 'Win': ", len(self.df['Win']))

        # self.df = pd.get_dummies(self.df, drop_first=False, 
        #                 columns=['Exchange', 'Exchange Amount', 'Card Before 3', 'Card Before 4', 'Card Before 5'])
    
        #fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(17, 5))
        # ax1.hist(self.df['Card Before 3'], label='Card Before 3')
        # ax2.hist(self.df['Card Before 4'], label='Card Before 4')
        # ax3.hist(self.df['Card Before 5'], label='Card Before 5')
        # ax4.hist(self.df['Win'], label='Win')
        #plt.show()
        
        # print(self.df)
        # fig, (ax1) = plt.subplots(1, 1, figsize=(17, 5))
        # ax1.hist(self.df['Exchange_False'], label='Exchange')
        # plt.show()

        # sns.set_theme(style="darkgrid")
        # tdc =sns.scatterplot(x = 'Exchange_False', y = self.df.index[:500], 
        # data = self.df[:500], hue = 'Win')
        # tdc.legend(loc='center left',
        # bbox_to_anchor=(1.0, 0.5), ncol=1)
        # plt.show()
        # ----------------------------------------------------------------------
        if self.win_or_not == True:
            self.X = self.df.drop(columns=["Win"], axis=1)
            self.y = self.df["Win"]
        
        # --------------------------------------- EXCHANGE AMOUNT PREDICTION ---------------------------------------
        if self.exchange_or_not == True: 
            self.X = self.df.drop(columns=["Exchange Amount", "Win"], axis=1)
            #self.X = self.df.drop(columns=["Win"], axis=1)
            print(len(self.X))
            self.y = self.df["Exchange Amount"]
        # ----------------------------------------------------------------------------------------------------------

        # print(self.X)
        if self.win_or_not == True:
            self.X = pd.get_dummies(self.X, columns=["Exchange Amount"], drop_first=False)
            
            if 'Exchange Amount_0' not in self.X.columns:
                self.X['Exchange Amount_0'] = 0
            if 'Exchange Amount_2' not in self.X.columns:
                self.X['Exchange Amount_2'] = 0
            if 'Exchange Amount_3' not in self.X.columns:
                self.X['Exchange Amount_3'] = 0 
        
        if self.exchange_or_not == True:
            self.y = pd.get_dummies(self.y, columns=["Exchange Amount"], drop_first=False)

            if 0 not in self.y.columns:
                self.y['Exchange Amount_0'] = 0
            else:
                self.y.rename(columns={ 0 : 'Exchange Amount_0'}, inplace=True)
                            
            if 2 not in self.y.columns:
                self.y['Exchange Amount_2'] = 0
            else:
                self.y.rename(columns={ 2 : 'Exchange Amount_2'}, inplace=True)
            
            if 3 not in self.y.columns:
                self.y['Exchange Amount_3'] = 0
            else:
                self.y.rename(columns={ 3 : 'Exchange Amount_3'}, inplace=True)
        
        self.X = self.X.astype(np.int64)
        self.y = self.y.astype(np.int64)

        print(self.X)
        print(self.y)

        # scaler = MinMaxScaler()
        # X_norm = pd.DataFrame(scaler.fit_transform(self.X), columns=self.X.columns)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, 
                                                                                self.y, 
                                                                                test_size=0.2, 
                                                                                random_state=10)

# def learning_rate_test(learning_rate, X_train, y_train):
#     #Step 1: Model configuration
#     model=Sequential(
#             [
#                 Input([len(X_train.columns)]),
#                 Dense(units=500, activation='relu', name='layer1'),
#                 Dense(units=500, activation='relu', name='layer2'),
#                 Dense(units=1, activation='relu', name='layer3')
#             ]
#         )

#     #Step 2: Compiling the model
#     #optimizer and evaluation metrics here
#     model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate), loss='binary_crossentropy', metrics=["accuracy"])

#     #Step 3: We fit our data to the model
#     callbacks = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10, verbose=1, restore_best_weights=True)
#     history=model.fit(X_train, y_train,epochs=50, validation_split=0.2,callbacks=[callbacks])
#     score=model.evaluate(X_train, y_train)
    
#     return score[1]

    def train_with_optimizer(self, X_train, y_train, optimizer, learning_rate):     
        model=Sequential(
                [
                    Input(shape=[len(X_train.columns),], name = 'input_layer'),
                    Dense(units=512, activation='relu', name='layer1'),
                    tf.keras.layers.Dropout(0.2),               
                    Dense(units=256, activation='relu', name='layer2'),
                ]
            )
        
        if self.win_or_not == True:
            model.add(Dense(units=1, activation='sigmoid', name='binary_output'))
            
        if self.exchange_or_not == True:
            model.add(Dense(units=3, activation='sigmoid', name='binary_output'))

        model.compile(optimizer=optimizer(
                    learning_rate=learning_rate),
                    loss=["binary_focal_crossentropy",],                
                    metrics=["accuracy"])
        
        model.summary()

        callbacks = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10)
                
        history = model.fit(X_train, y_train, batch_size=32, epochs = 222, callbacks=[callbacks], validation_split = 0.2)
        
        test_loss, test_acc = model.evaluate(X_train, y_train)

        print('Test Accuracy: ', test_acc)
        print('Test Loss: ', test_loss)
        
        return model, history, test_acc, test_loss

    def ml_learning_and_prediction(self):        
        # Create an empty list to store the accuracies
        accuracies = []
        losses = []
        
        optimizers = [tf.keras.optimizers.Adam, 
                    tf.keras.optimizers.RMSprop, 
                    tf.keras.optimizers.SGD, 
                    tf.keras.optimizers.Adadelta]
        
        # Try out different learning rates
        learning_rates = [0.00001]
        
        optimizer = tf.keras.optimizers.Adam
        
        opt = 'Adam'
        l_r = '00001'
        
        idx = 2
        # Loop through the different optimizers
        for rate in learning_rates:
            model, history, test_acc, test_loss = self.train_with_optimizer(
                self.X_train, self.y_train, optimizer, rate)
            
            # Append the accuracy to the list
            accuracies.append(test_acc)
            losses.append(test_loss)
            self.visualize_model(history)
            self.plot_loss_accuracy(history)
            
            date_now = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            if self.win_or_not == True:
                model.save('models_prediction/model_base_WIN' + '_' + opt + '_' + l_r + '_test_acc=' + str("{:.3f}".format(test_acc)) + '_test_loss=' + str("{:.3f}".format(test_loss)) + '_' + date_now + '.keras')
            if self.exchange_or_not == True:
                model.save('models_prediction/model_base_EX_AMOUNT' + '_' + opt + '_' + l_r + '_test_acc=' + str("{:.3f}".format(test_acc)) + '_test_loss=' + str("{:.3f}".format(test_loss)) + '_' + date_now + '.keras')

            idx += 1

        print(accuracies)
        print(losses)
        
        if self.win_or_not == True:
            self.y_preds = model.predict(self.X_test).flatten()
            
            #self.y_preds = (self.y_preds > 0.5).astype(int)        
            
            df_predictions = pd.DataFrame({'Ground_Truth (Win)': self.y_test, 'Model_prediction (Win)': self.y_preds}, 
                                        columns=['Ground_Truth (Win)', 'Model_prediction (Win)'])

            date_now = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            df_predictions.to_excel("models_prediction/preds_win_or_not_" + date_now + '.xlsx')
            
        # --------------------------------------- EXCHANGE AMOUNT PREDICTION ---------------------------------------     
        if self.exchange_or_not == True:     
            self.y_preds = model.predict(self.X_test)

            y1 = pd.DataFrame()
            y1 = self.y_test['Exchange Amount_0']
            y2 = pd.DataFrame()
            y2 = self.y_test['Exchange Amount_2']       
            y3 = pd.DataFrame()
            y3 = self.y_test['Exchange Amount_3']
            
            df_predictions = pd.DataFrame({'Ground_Truth (0)': y1,
                                        'Ground_Truth (2)': y2,
                                        'Ground_Truth (3)': y3, 
                                        'Model_prediction (0)': [self.y_preds[idx][0] for idx in range(len(self.y_preds))],
                                        'Model_prediction (2)': [self.y_preds[idx][1] for idx in range(len(self.y_preds))],
                                        'Model_prediction (3)': [self.y_preds[idx][2] for idx in range(len(self.y_preds))]
                                        }, 
                                        columns=['Ground_Truth (0)', 'Ground_Truth (2)',
                                                    'Ground_Truth (3)',
                                                    'Model_prediction (0)', 'Model_prediction (2)',
                                                    'Model_prediction (3)'])
            
            date_now = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            df_predictions.to_excel("models_prediction/preds_ex_amount_" + date_now + '.xlsx')

        # ----------------------------------------------------------------------------------------------------------
            
        print(df_predictions) 
    
    def update_model(self, base_model_path):
        
        if os.path.exists(base_model_path):
            model = load_model(base_model_path)
        else:
            print("Plik z modelem aktualizacja/baza nie istnieje.")
            return
      
        self.pre_processing()
        
        callbacks = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10)
        
        model.summary()
       
        history = model.fit(self.X_train, self.y_train, batch_size=32, epochs = 222, callbacks=[callbacks], validation_split = 0.1)
        
        test_loss, test_acc = model.evaluate(self.X_train, self.y_train)
        
        
        print('Test Accuracy: ', test_acc)
        print('Test Loss: ', test_loss)
        
        self.visualize_model(history)
        self.plot_loss_accuracy(history)
        
        date_now = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        
        if self.win_or_not == True:
            self.filename_updated = 'models_prediction/model_updated_WIN' + '_' + self.opt + '_' + self.l_r + '_test_acc=' + str("{:.3f}".format(test_acc)) + '_test_loss=' + str("{:.3f}".format(test_loss)) + '_' + date_now + '.keras'
            
            with open('models_prediction/path_to_model_WIN.txt', 'w') as file:
                file.write(self.filename_updated)
            
            model.save(self.filename_updated)
            
        if self.exchange_or_not == True:
            self.filename_updated = 'models_prediction/model_updated_EX_AMOUNT' + '_' + self.opt + '_' + self.l_r + '_test_acc=' + str("{:.3f}".format(test_acc)) + '_test_loss=' + str("{:.3f}".format(test_loss)) + '_' + date_now + '.keras'
            
            with open('models_prediction/path_to_model_EX_AMOUNT.txt', 'w') as file:
                file.write(self.filename_updated)
            
            model.save(self.filename_updated)
            
        # --------------------------------------- WIN OR NOT PREDICTION ---------------------------------------     
        if self.win_or_not == True:
            self.y_preds = model.predict(self.X_test).flatten()
            
            #self.y_preds = (self.y_preds > 0.5).astype(int)        
            
            df_predictions = pd.DataFrame({'Ground_Truth (Win)': self.y_test, 'Model_prediction (Win)': self.y_preds}, 
                                        columns=['Ground_Truth (Win)', 'Model_prediction (Win)'])

            date_now = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            df_predictions.to_excel("models_prediction/preds_win_or_not_" + date_now + '.xlsx')
            
        # --------------------------------------- EXCHANGE AMOUNT PREDICTION ---------------------------------------     
        if self.exchange_or_not == True:     
            self.y_preds = model.predict(self.X_test)

            y1 = pd.DataFrame()
            y1 = self.y_test['Exchange Amount_0']
            y2 = pd.DataFrame()
            y2 = self.y_test['Exchange Amount_2']       
            y3 = pd.DataFrame()
            y3 = self.y_test['Exchange Amount_3']
            
            df_predictions = pd.DataFrame({'Ground_Truth (0)': y1,
                                        'Ground_Truth (2)': y2,
                                        'Ground_Truth (3)': y3, 
                                        'Model_prediction (0)': [self.y_preds[idx][0] for idx in range(len(self.y_preds))],
                                        'Model_prediction (2)': [self.y_preds[idx][1] for idx in range(len(self.y_preds))],
                                        'Model_prediction (3)': [self.y_preds[idx][2] for idx in range(len(self.y_preds))]
                                        }, 
                                        columns=['Ground_Truth (0)', 'Ground_Truth (2)',
                                                    'Ground_Truth (3)',
                                                    'Model_prediction (0)', 'Model_prediction (2)',
                                                    'Model_prediction (3)'])
            
            date_now = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            df_predictions.to_excel("models_prediction/preds_ex_amount_" + date_now + '.xlsx')
   
        
        
    def plot_loss_accuracy(self, history_1):
        # Extract the loss and accuracy history for both training and validation data
        loss = history_1.history['loss']
        val_loss = history_1.history['val_loss']
        acc = history_1.history['accuracy']
        val_acc = history_1.history['val_accuracy']
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 6))
        # Plot the loss history
        ax1.plot(loss, label='Training loss')
        ax1.plot(val_loss, label='Validation loss')
        ax1.set_title('Loss history')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        
        # Plot the accuracy history
        ax2.plot(acc, label='Training accuracy')
        ax2.plot(val_acc, label='Validation accuracy')
        ax2.set_title('Accuracy history')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        plt.show()
        
    def visualize_model(self, history, y_min = None, y_max = None):
        print(history.history.keys())
        plt.figure()
        plt.plot(history.history['loss'])
        plt.title('Model loss')
        plt.xlabel('Number of epochs')
        plt.ylabel('Loss')
        plt.ylim([y_min, y_max])
        plt.legend(['loss plot'], loc='upper right')
        plt.show()
