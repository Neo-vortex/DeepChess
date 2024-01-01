import sqlite3
import numpy as np
import tensorflow as tf
import base64



def bin_to_input(bin):
    binq = np.frombuffer(bin, dtype=np.uint8)
    binq = np.unpackbits(binq, axis=0).astype(np.single) 
    return binq

    piece_to_index = {'p': 0, 'r': 1, 'n': 2, 'b': 3, 'q': 4, 'k': 5, 'P': 6, 'R': 7, 'N': 8, 'B': 9, 'Q': 10, 'K': 11}
    board = np.zeros((8, 8, 13), dtype=np.uint8)  # Updated to 13 to include the side to move
    board_state, turn, castling, en_passant, halfmove, fullmove = fen.split()

    side_to_move = 0 if turn == 'b' else 1  # Updated to correctly assign side to move

    row, col = 0, 0
    for char in board_state:
        if char == '/':
            row += 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            piece_index = piece_to_index[char]
            board[row, col, piece_index] = 1
            col += 1

    # Add side-to-move information to the input
    board[:, :, 12] = side_to_move  # Updated index for side to move

    return board

def predict_score(model, fen):
    tmp = (bin_to_input(fen),)
    score = model.predict(tf.expand_dims(tmp, axis=-1))[0][0]
    return score

# Load the pre-trained model
model = tf.keras.models.load_model('chess_model.h5')


fen = "AgAAAAAAAAAAAAAAAAAAAAQAAAAQAAAAAAAAAAAAAAAAAAQAAAAAAACnACAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAACBAAAAAAAAQAAAAAAAAAAAAAAAAAAIUIcAAAAB/wA="

# Decode the base64 string into a byte array
byte_array = base64.b64decode(fen)


# Make a prediction
predicted_score = predict_score(model, byte_array)

print(f'Predicted Score for position "{fen}": {predicted_score  }')