from classes.Croupier import Croupier
from classes.Player import Player
from decision_tree_structure.OnePairStructureStrategy import OnePairStructureStrategy
import time
import cProfile
import pstats
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler 
def plot_loss_accuracy(history_1):
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
    
def visualize_model(history, y_min = None, y_max = None):
    print(history.history.keys())
    plt.figure()
    plt.plot(history.history['loss'])
    plt.title('Model loss')
    plt.xlabel('Number of epochs')
    plt.ylabel('Loss')
    plt.ylim([y_min, y_max])
    plt.legend(['loss plot'], loc='upper right')
    plt.show()

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

def train_with_optimizer(X_train, y_train, optimizer, learning_rate, epsilon, beta1, beta2, callbacks=[]):
    mobilenet = tf.keras.applications.MobileNet(weights='imagenet', include_top=False, input_shape=(1, 12))
    # Freeze all layers in the MobileNet model
    for layer in mobilenet.layers:
        layer.trainable = False
        
    # Struktura modelu
    model=Sequential(
            [
                Input([len(X_train.columns)]),
                Dense(units=1024, activation='relu', name='layer1'),
                tf.keras.layers.Dropout(0.5),
                Dense(units=128, activation='relu', name='layer2'),
                Dense(units=128, activation='relu', name='layer3'),
                Dense(units=1, activation='hard_sigmoid', name='layer4')
            ]
        )
   
    model.compile(optimizer=optimizer(
                  learning_rate=learning_rate, 
                  epsilon=epsilon, 
                  beta_1=beta1, 
                  beta_2=beta2), 
                  loss="binary_focal_crossentropy", 
                  metrics=["accuracy"])

    model.summary()
#    np.argmax(predictions[0]),test_labels[0]

    callbacks = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=20, verbose=1, restore_best_weights=True)

    history = model.fit(X_train, y_train, epochs = 1000, callbacks=[callbacks],
                          validation_split = 0.2)

    test_loss, test_acc = model.evaluate(X_train, y_train)
    
    print('Test Accuracy: ', test_acc)

    return model, history, test_acc, test_loss

def main():
    start_time = time.time()
    
    cards_1, rand_int_1, all_comb_perm = Player().cards_permutations()
    for i in range(0, 10000):
        croupier = Croupier(all_comb_perm)
        print(i)
        croupier.play()
    
    
    
    
    # df = pd.read_csv('poker_game.csv', on_bad_lines='skip', engine='python')
    # pd.set_option('display.max_columns', 16)
    
    # pd.options.display.float_format = '{:,.0f}'.format
    # df = df.fillna('0')
    # # df['Exchange'] = df['Exchange'].replace({'[\'t\']': True, '[\'n\']': False})
    
    # df.loc[df['Exchange'] == '[\'t\']', 'Exchange'] = 1
    # df.loc[df['Exchange'] == '[\'n\']', 'Exchange'] = 0


    # df.loc[df['Exchange Amount'] == '[0]', 'Exchange Amount'] = 0
    
    # df.loc[df[' Cards Exchanged 1'] == '', ' Cards Exchanged 1'] = 0
    # df.loc[df[' Cards Exchanged 2'] == '', ' Cards Exchanged 2'] = 0
    # df.loc[df[' Cards Exchanged 3'] == '', ' Cards Exchanged 3'] = 0



    # #print(df.head().corr())
    # df = df.rename(columns={' Card After 1': 'Card After 1', ' Card After 2': 'Card After 2', ' Card After 3': 'Card After 3', 
    #                         ' Card After 4': 'Card After 4', ' Card After 5': 'Card After 5',
    #                         ' Cards Exchanged 1': 'Cards Exchanged 1', ' Cards Exchanged 2': 'Cards Exchanged 2',
    #                         ' Cards Exchanged 3': 'Cards Exchanged 3'})
    # # #df = df.head()
    # # df.drop(columns=['Card After 1', 'Card After 2', 'Card After 3', 'Card After 4', 'Card After 5',
    # #                     'Cards Exchanged 1', 'Cards Exchanged 2', 'Cards Exchanged 3',
    # #                     'Arrangement ID (After)'], axis=1, inplace=True)
    
    # df.drop(columns=['Card After 1','Card After 2','Card After 3', 'Card After 4', 'Card After 5', 'Arrangement ID (After)'], axis=1, inplace=True)
  
    
    

    
    # df = pd.get_dummies(df, drop_first=False, columns=['Exchange', 'Exchange Amount'])
    
    # print(df['Win'])
    # print(df[' Card Before 2'])
    # plt.figure()
    # plt.scatter(df[' Card Before 2'].values, df['Win'].values)
    # plt.show()
    
    # #df.to_excel('poker_game_out.xlsx', index=True)
    # #df.to_csv('poker_game_out.csv', index=True)
    
    # # X = df.drop("Weight", axis=1) 
    # # X = df.drop("Weight (After)", axis=1)
    
    
    # df.drop(columns=["Weight", "Weight (After)"], axis=1, inplace=True)
    
    # X = df.drop("Win", axis=1)
    # # X = df.drop("Weight (After)", axis=1, inplace=True)
    # # X = df.drop("Win", axis=1)
    # y = df["Win"]
    
    
    
    # print(X.head())
    # print(len(X))
    # print(len(y))
    # print(X.shape)
    # print(y.shape)
    
    # X = X.astype(np.int64)
    # y = y.astype(np.int64)
    
    # # create a scaler object
    # #scaler = MinMaxScaler()
    
    # # fit and transform the data
    # # X_norm = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    # # print(X_norm.head())
    # # X_norm.describe()
    
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    
    # # df = df.head().corr()
    # # df.to_excel('corr.xlsx', index=False)
    
    # # model_1 = Sequential(
    # #     [
    # #         Input([len(X_train.columns)]),
    # #         Dense(units=64, activation='sigmoid', name='layer1'),
    # #         Dense(units=64, activation='sigmoid', name='layer2'),
    # #         Dense(units=64, activation='sigmoid', name='layer3'),
    # #         Dense(units=1, activation='sigmoid', name='layer4')
    # #     ]
    # # )
    # # early_stop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10)

    # # # Kompilacja modelu
    # # model_1.compile(loss='binary_crossentropy', optimizer='Adam', metrics = ['accuracy'])

    # # #Dopasowywanie modelu
    # # history_1 = model_1.fit(X_train, y_train, epochs = 500, callbacks=[early_stop])
    
    # # model_1.save('model_1.keras')
    
    # # Try out different learning rates
    # learning_rates = [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
    # # Create an empty list to store the accuracies
    # accuracies = []
    # # Loop through the different learning rates
    # # for learning_rate in learning_rates:
    # #     # Get the accuracy for the current learning rate
    # #     accuracy = learning_rate_test(learning_rate, X_train, y_train)
    # #     # Append the accuracy to the list
    # #     accuracies.append(accuracy)

    # optimizers = [tf.keras.optimizers.Adam, tf.keras.optimizers.RMSprop, tf.keras.optimizers.SGD, tf.keras.optimizers.Adadelta]
    # optimizers = [tf.keras.optimizers.Adam]
    # # # Create an empty list to store the accuracies
    # accuracies = []
    # losses = []
  
 
    # # Loop through the different optimizers
    # for opt in optimizers:
    #     # Get the accuracy for each optimizer
    #     model, history, test_acc, test_loss = train_with_optimizer(
    #         X_train, y_train, opt, learning_rate=0.0001, epsilon=1e-07, beta1=0.7, beta2=0.999)
    #     # Append the accuracy to the list
    #     accuracies.append(test_acc)
    #     losses.append(test_loss)
    #     visualize_model(history)
    #     plot_loss_accuracy(history)
        
    # print(accuracies)
    # print(losses)
    
    # #opt = tf.keras.optimizers.Adam
    
    # #model, history, test_acc, test_loss = train_with_optimizer(X_train, y_train, opt, learning_rate=0.001)
    # #visualize_model(history)
    
    # # model_2 = Sequential(
    # #     [
    # #         Input([len(X_train.columns)]),
    # #         Dense(units=500, activation='relu', name='layer1'),
    # #         Dense(units=500, activation='relu', name='layer2'),
    # #         Dense(units=1, activation='relu', name='layer3')
    # #     ]
    # # )
    # # early_stop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10)

    # # # Kompilacja modelu
    # # model_2.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.000001), metrics = ['accuracy'])

    # # #Dopasowywanie modelu
    # # history_2 = model_2.fit(X_train, y_train, epochs = 500, callbacks=[early_stop])
    
    # # # visualize_model(history_1)
    # # visualize_model(history_2)
    
    # # y_preds = model_2.predict(X_test).flatten()
    # y_preds = (y_preds > 0.5).astype(int)
    
    # df_predictions = pd.DataFrame({'Ground_Truth': y_test, 'Model_prediction': y_preds}, 
    #                               columns=['Ground_Truth','Model_prediction']) 
    # df_predictions['Model_prediction'] = df_predictions['Model_prediction'].astype(np.float64)
    
    # print(df_predictions) 
    
    # df_predictions.to_excel('predictions.xlsx')

    end_time = time.time() - start_time
    with open("time.txt", "w") as file:
        file.write(str(end_time) + " sec\n")
    
    print()    
    print(end_time, " sec")
    
if __name__ == "__main__":
    #cProfile.run('main()', 'full_profiler.txt')
    
    main()
    
    #p = pstats.Stats('full_profiler.txt')
    #p.sort_stats('cumulative').print_stats()