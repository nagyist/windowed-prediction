# Directory Structure

├── edge_prediction
│   ├── data
│   │   ├── train-input
│   │   └── train-labels
│   ├── edge_prediction_conv
│   ├── results
│   └── util
├── lib
└── util


# Edge Prediction
Convolutional network that performs edge detection by using segmented labeled training data. 

There are two ways to run the code from within the edge_prediction directory:

## Option 1 (fast)
1. Run `python edge_prediction --small/medium/large` to generate training/test data, and to predict edges.
2. Or run `python edge_prediction --small/medium/large` to only perform edge prediction.
3. The training time is set to 100 epochs. To train for a shorter period, press `Ctrl+C` to throw a KeybordInterrupt and the program will exit the training loop and start the prediction on the test set. 
4. Run `plot.py`n to plot a visual prediction from the test set, where the integer n is
   a member of the test set.

## Option 2
1. Place training data in `synapse_train_data/train_input`
2. Place training labels in `synapse_train_data/train_labels`
3. Run `python edge_prediction --pre-process --small/medium/large` to generate training/test data, and to predict edges.
4. Or run `python edge_prediction --small/medium/large` to only perform edge prediction.
5. The training time is set to 100 epochs. To train for a shorter period, press `Ctrl+C` to throw a KeybordInterrupt and the program will exit the training loop and start the prediction on the test set. 
6. Run `plot.py`n to plot a visual prediction from the test set, where the integer n is
   a member of the test set.

Small, medium and large are convolutional network with 10,64 and 100 filters per
convolution. The train/test set for the three options are 1500/500, 4000/1000
and 9000/1000, respectively. In all cases, the validation set is of size 200
and is a subset of the test set. The number of neurons in the fully connected layer is always the same as the number of outputs in the last convolutional layer.
