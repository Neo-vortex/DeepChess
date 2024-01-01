import base64
import sqlite3
import numpy as np
import tensorflow as tf


conn = sqlite3.connect('./dataset/chess_evals.db' , check_same_thread= False)
cursor = conn.cursor()
model = tf.keras.models.load_model("chess_model.h5")

print(model.summary())


def bin_to_input(bin):
    bin = base64.b64decode(bin)
    binq = np.frombuffer(bin, dtype=np.uint8)
    binq = np.unpackbits(binq, axis=0).astype(np.single) 
    return binq

def fetch_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT binary, eval FROM evaluations ORDER BY  RANDOM() LIMIT 1000000")
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