# Deep Learning Chess Engine Project

## Introduction
Hello, Chess and AI enthusiasts! I'm excited to share my deep learning project focused on chess. As a hobby chess player with a Lichess rating of 1500, my fascination with chess led me to explore the intersection of this ancient game and modern artificial intelligence. While I'm not an AI expert, my curiosity and foundational understanding of key AI concepts and tools have been the driving force behind this project.

## Project Overview
The goal of this project was modest yet ambitious: to create a functional chess engine using deep learning techniques. Recognizing the complexities and the advanced nature of existing chess engines, my aim was not to surpass them but to build a competent and learning-based engine. This project was executed on my personal machine, equipped with an Intel i7 12700, 32 GB DDR4 RAM, and an RTX 3060 12GB, running Ubuntu.

## Methodology
### Data Collection and Preparation
- **Source:** Utilized the Lichess database ([Lichess Database](https://database.lichess.org/)), which contains games played on Lichess since 2013.
- **Dataset:** Selected the first five months of 2013, translating into about 750,000 games and 23 million non-unique FEN positions. evaluted with stockfish 16 at depth ** 8 **
- **Tools:** Employed `pgn-extract` ([pgn-extract](https://github.com/MichaelB7/pgn-extract)) for processing the games and a Go library ([notnil/chess](https://github.com/notnil/chess)) for encoding FEN positions to binary.
- **Implementation:** Developed a C# project for integrating with the Go library and storing the data in a SQLite database.

### Model Training
- **Framework:** TensorFlow and Keras with CUDA for GPU acceleration.
- **Architecture:** Implemented a CNN with 20 Dense layers, each followed by BatchNormalization, ReLU, and 0.3 Dropout.
- **Training:** Originally planned for 30 epochs but stopped at 15 due to overfitting concerns.

### Results
- **Model Parameters:** 13,138,889 total; 13,106,569 trainable.
- **Performance Metrics:**
  - Mean Squared Error (MSE): 57900.645
  - Root Mean Squared Error (RMSE): 240.625
  - Mean Absolute Error (MAE): 119.149
  - R-squared: 0.837447
- **Correlation between True Score and Predicted Score:** 0.915121



# Model Architecture

In this section, we delve into the architecture of the deep learning model employed in this chess engine project. The model is constructed using TensorFlow and Keras, and it's designed to evaluate chess positions efficiently. Here's a closer look at the code responsible for building the model:

```python
import tensorflow as tf

# Define the input shape and layer sizes
input_shape = (808,)
layer_sizes = [808,  808 , 808 , 808, 808, 808, 808, 808, 808, 808, 808, 808, 808, 808, 808, 808, 808, 808, 808, 808]  # Adjust the layer sizes as needed

# Initialize the layers list with the input layer
layers = [tf.keras.layers.InputLayer(input_shape=input_shape)]

# Construct the hidden layers
for i, size in enumerate(layer_sizes):
    layers.append(tf.keras.layers.Dense(size, name=f"linear-{i}"))
    layers.append(tf.keras.layers.BatchNormalization(name=f"batch_norm-{i}"))
    layers.append(tf.keras.layers.ReLU(name=f"relu-{i}"))
    layers.append(tf.keras.layers.Dropout(0.3, name=f"dropout-{i}"))

# Add the output layer with linear activation for regression
layers.append(tf.keras.layers.Dense(1, activation='linear', name=f"linear-{len(layer_sizes)}"))

# Create the Sequential model
model = tf.keras.Sequential(layers)
```


### Input Layer
- **Purpose**: Initialize the input layer with the shape of input data. as the FEN encoder, encodes data to 808 binary elemets
- **Code**: 
  ```python
  tf.keras.layers.InputLayer(input_shape=input_shape)
  ```

### Hidden Layers
- **Design**: Iteratively construct hidden layers to process the input data.
- **Components**:
  - **Dense Layer**: 
    - Fully connected layer.
    - Code: 
      ```python
      tf.keras.layers.Dense(size, name=f"linear-{i}")
      ```
  - **Batch Normalization**:
    - Normalizes the activations from the previous layer.
    - Code: 
      ```python
      tf.keras.layers.BatchNormalization(name=f"batch_norm-{i}")
      ```
  - **ReLU Activation**:
    - Adds non-linearity to the model.
    - Code: 
      ```python
      tf.keras.layers.ReLU(name=f"relu-{i}")
      ```
  - **Dropout**:
    - Prevents overfitting by randomly setting a fraction of the inputs to zero.
    - Code: 
      ```python
      tf.keras.layers.Dropout(0.3, name=f"dropout-{i}")
      ```

### Output Layer
- **Purpose**: Provide the final regression output.
- **Code**:
  ```python
  tf.keras.layers.Dense(1, activation='linear', name=f"linear-{len(layer_sizes)}")
  ```

### Model Assembly
- **Method**: Sequentially stacking the layers.
- **Code**:
  ```python
  model = tf.keras.Sequential(layers)
  ```


![Figure_1](https://github.com/Neo-vortex/DeepChess/assets/40230471/f1eb8d86-c68d-4d20-924e-ad15d4a8628a)

![Figure_2](https://github.com/Neo-vortex/DeepChess/assets/40230471/2027bf94-b090-4079-b04d-41c20a859622)

![Figure_3](https://github.com/Neo-vortex/DeepChess/assets/40230471/9f98515f-296b-4e80-b1f4-6e598853aad9)

## Project Building Requirements
To successfully build and run this chess engine project, certain software and tools are required. Below is a list of the necessary prerequisites and their respective versions. Ensure that these are installed and properly set up on your development environment before proceeding with the project setup.

### Software and Tools
* .NET 8: The project utilizes .NET 8 for certain components, particularly in areas interfacing with the Go library and handling data processing. Ensure that you have the latest version of .NET 8 installed. You can download it from the official .NET website.

* Go 1.20+: Go programming language is used, especially for handling chess logic and FEN position encoding. Version 1.20 or higher is required. Download the latest version of Go from the official Go website.

* Python 3.12: The deep learning model is implemented in Python, utilizing libraries such as TensorFlow and Keras. Python 3.12 is the minimum required version. Download Python from the official Python website.

* Conda: Conda is used for managing Python dependencies and environments. It is highly recommended for isolating and managing project-specific packages. Download Conda from the official Conda website.

* Make: A build automation tool that simplifies the compilation process. Make sure you have 'make' installed for handling the build scripts. It is usually pre-installed on Linux and macOS. For Windows, it can be installed via various package managers.

* GCC or Other C Compiler: A C compiler is necessary for parts of the project that involve C code, such as fen-extractor . GCC is recommended, but any standard C compiler should suffice. GCC can be installed from the GCC official website or through your system's package manager.

** More info about how to setup and use the actual code comes soon!

## Show Me Some Games
Ok!

This is the first game I played with DeepChess I used alpha-beta searching but I set the depth to 1 to start! not so impresive.
As expected, it did no go so well and the engine blundered a knight in the very early moves 

[White : neo, Black : DeepChess(depth=1), no time control]
![game1](https://github.com/Neo-vortex/DeepChess/assets/40230471/446e1303-6c06-48c9-aedc-233e48dfe6b4)


Let's see how it performs with depth = 3

[White : neo, Black : DeepChess(depth=3), no time control]
![2](https://github.com/Neo-vortex/DeepChess/assets/40230471/ef29819c-4cbd-45d9-a8ce-4f2dbf806cb2)

I did not play well at all in game 2, but I was impressed by how black can play and see the opportunities (forking, wining material , controlling semi-open files and counter attacks)!

## TODO :
* More games comming soon
* Provide the model publicly
* Deep dive into how to train and work with the code


