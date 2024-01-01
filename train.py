import base64
import os
import sqlite3
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.layers import Conv2D, Flatten, Dense , BatchNormalization , Dropout
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping , ReduceLROnPlateau, ModelCheckpoint
from keras.optimizers import Adam
from keras.regularizers import l2


batch_size = 4096
def bin_to_input(bin):
    bin = base64.b64decode(bin)
    binq = np.frombuffer(bin, dtype=np.uint8)
    binq = np.unpackbits(binq, axis=0).astype(np.single) 
    return binq

# Generator function for batch processing
def batch_generator(sqlite_connection, batch_size):
   

    while True:
        cursor.execute("SELECT  binary, eval FROM evaluations")
        while True:
            batch_data = cursor.fetchmany(batch_size)
            if not batch_data:
                break
            bins, y_batch = zip(*batch_data)

            X_batch_processed = np.array([bin_to_input(bin) for bin in bins])
            y_batch_processed = np.array(y_batch)
            #y_batch_processed = np.clip(y_batch_processed, -20.0, 20.0)
            yield X_batch_processed, y_batch_processed

input_shape = (808,)



layer_sizes = [808,  808 , 808 , 808,808, 808,808,808,808,808,808,808,808,808,808,808,808,808,808,808]  # Adjust the layer sizes as needed

layers = [tf.keras.layers.InputLayer(input_shape=input_shape)]

for i, size in enumerate(layer_sizes):
    layers.append(tf.keras.layers.Dense(size, name=f"linear-{i}"))
    layers.append(tf.keras.layers.BatchNormalization(name=f"batch_norm-{i}"))
    layers.append(tf.keras.layers.ReLU(name=f"relu-{i}"))
    layers.append(tf.keras.layers.Dropout(0.3, name=f"dropout-{i}"))

# Use linear activation for the output layer for regression
layers.append(tf.keras.layers.Dense(1, activation='linear', name=f"linear-{len(layer_sizes)}"))

model = tf.keras.Sequential(layers)


optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=0.001,
    decay_steps=10000,
    decay_rate=0.9
)
optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
# Compile the model
model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mae'])

#model.build
dot_img_file = 'model.png'
keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)
# Callbacks
early_stopping = EarlyStopping(monitor='loss', patience=5)
#reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=3, min_lr=0.005)

# Connect to SQLite database
conn = sqlite3.connect('./dataset/chess_evals.db' , check_same_thread= False)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(fen) FROM evaluations")
total_rows = cursor.fetchone()[0]
# Create the generator
train_generator = batch_generator(conn, batch_size)

# Train the model
steps_per_epoch = np.ceil(total_rows / batch_size)
model_checkpoint = ModelCheckpoint(
    'checkpoints/chess_model_checkpoint.h5', 
    save_best_only=True, 
    monitor='mae', 
    mode='min'
)

model.fit(train_generator, steps_per_epoch=steps_per_epoch, epochs=30, callbacks=[early_stopping, model_checkpoint])

# Save the model for later use
model.save('chess_model.h5')

# Close database connection
def fetch_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT binary, eval FROM evaluations ORDER BY  RANDOM() LIMIT 100000")
    data = cursor.fetchall()
    bins, y_batch = zip(*data)

    X_batch_processed = np.array([bin_to_input(bin_data) for bin_data in bins])
    y_batch_processed = np.array(y_batch)
    #y_batch_processed = np.clip(y_batch_processed, -20.0, 20.0)

    return X_batch_processed, y_batch_processed


def evaluate_and_write_results(model, X_data, true_scores, output_file):
    predicted_scores = model.predict(X_data)
    results = list(zip(true_scores, predicted_scores.flatten()))

    # Write results to a file
    with open(output_file, 'w') as f:
        f.write("True_Score, Predicted_Score\n")
        for true_score, predicted_score in results:
            f.write(f"{true_score}, {predicted_score}\n")

            
X_data, true_scores = fetch_all_data(conn)

    # Evaluate and write results to a file
evaluate_and_write_results(model, X_data, true_scores, 'evaluation_results.csv')

conn.close()