from lolDataProcessor import lolDataProcessor as dataProc
import customErrors as cE
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import pickle

def download_images(version_start, version_end):
    ''' Script to download the champion images based on the lolDataProcessor class'''
    try:
        data_proc = dataProc()
        data_proc.fetch_champions("data")

        # The actual location of the images is not clear, so in the range (0 - 65), it will cover roughly 1700+ skins
        for version in range(version_start, version_end):
            data_proc.downloadAllChampions(str(version))

    except cE.FailFetch as ff:
        print(f"Error: {ff}")
    except cE.EmptyChampionList as ecl:
        print(f"Error: {ecl}")

def load_proc_data():
    data_directory = os.getcwd() + '\\' + 'tags'
    data_gen = ImageDataGenerator(rescale=1.0/255, validation_split=0.2)

    train_data = data_gen.flow_from_directory(
        data_directory,
        target_size=(600, 354),
        batch_size=30,
        class_mode='categorical',
        shuffle=True,
        subset='training'
    )
    val_data = data_gen.flow_from_directory(
        data_directory,
        target_size=(600, 354),
        batch_size=30,
        class_mode='categorical',
        shuffle=True,
        subset='validation'
    )
    return train_data, val_data

def build_model(input_shape, num_classes):
    model = Sequential()

    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))  

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy']
                  )

    return model

input_shape = (600, 354, 3)
num_classes = 6
train_data, val_data = load_proc_data()

checkpoint = ModelCheckpoint('trained_model_v1.h5', save_best_only=True)
early_stopping = EarlyStopping(patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(factor=0.1, patience=3)

model = build_model(input_shape, num_classes)
history = model.fit(train_data, epochs=20, 
            validation_data=val_data,
            callbacks=[checkpoint, early_stopping, reduce_lr]
            )

with open('train_history_v1.pkl', 'wb') as file:
    pickle.dump(history.history, file)
