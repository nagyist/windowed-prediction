from helper_functions import Functions
import theano
from lib.pool_layer                    import PoolLayer
from lib.hidden_layer                  import HiddenLayer
from lib.logistic_sgd                  import LogisticRegression
from lib.pool_layer import PoolLayer

class CovNet(Functions):
    '''
    Class that defines the hierarchy and design of the convolutional
    layers.
    '''
    
    def __init__(self, rng, batch_size,num_kernels,kernel_sizes,x,y,input_window_shape,output_window_shape,maxoutsize = 1):
        
        self.srng = theano.tensor.shared_randomstreams.RandomStreams(
                            rng.randint(999999))

        self.layer0_input_size  = (batch_size, 1, input_window_shape[0], input_window_shape[1])           # Input size from data 
        self.edge0              = (input_window_shape[0] - kernel_sizes[0][0] + 1)/ 2                     # New edge size
        self.layer0_output_size = (batch_size, num_kernels[0]/maxoutsize, self.edge0, self.edge0)                    # Output size
        assert ((input_window_shape[0] - kernel_sizes[0][0] + 1) % 2) == 0                                # Check pooling size
        
        # Initialize Layer 0
        #self.layer0_input = x.reshape(self.layer0_input_size)
        self.layer0_input = x.reshape((batch_size,1,input_window_shape[0],input_window_shape[1]))

        self.layer0 = PoolLayer(rng,
                                    input=self.dropout(self.layer0_input,p=0.2),
                                    image_shape=self.layer0_input_size,
                                    subsample= (1,1),
                                    filter_shape=(num_kernels[0], 1) + kernel_sizes[0],
                                    poolsize=(2, 2))

        self.layer1_input_size  = self.layer0_output_size                              # Input size Layer 1
        self.edge1              = (self.edge0 - kernel_sizes[1][0] + 1)/ 2            # New edge size
        self.layer1_output_size = (batch_size, num_kernels[1]/maxoutsize, self.edge1, self.edge1) # Output size
        assert ((self.edge0 - kernel_sizes[1][0] + 1) % 2) == 0                        # Check pooling size

        # Initialize Layer 1
        self.layer1 = PoolLayer(rng,
                                    input= self.dropout(self.layer0.output,p=0.2),
                                    image_shape=self.layer1_input_size,
                                    subsample= (1,1),
                                    filter_shape=(num_kernels[1], num_kernels[0]/maxoutsize) + kernel_sizes[1],
                                    poolsize=(2, 2))
                                    
        self.layer2_input_size  = self.layer1_output_size                              # Input size Layer 1
        self.edge2              = (self.edge1 - kernel_sizes[2][0] + 1)/2           # New edge size
        self.layer2_output_size = (batch_size, num_kernels[2]/maxoutsize, self.edge2, self.edge2) # Output size
        assert ((self.edge1 - kernel_sizes[2][0] + 1) % 2) == 0                        # Check pooling size

        # Initialize Layer 2
        self.layer2 = PoolLayer(rng,
                                    input= self.dropout(self.layer1.output,p=0.2),
                                    image_shape=self.layer2_input_size,
                                    subsample= (1,1),
                                    filter_shape=(num_kernels[2], num_kernels[1]/maxoutsize) + kernel_sizes[2],
                                    poolsize=(2, 2))

        self.layer3_input = self.layer2.output.flatten(2)
        
        # Layer 3: Fully connected layer
        self.layer3 = HiddenLayer(rng,
                                  input      = self.dropout(self.layer3_input,p=0.2),
                                  n_in       = num_kernels[2] * self.edge2 * self.edge2,
                                  n_out      = num_kernels[2] * self.edge2 * self.edge2,
                                  activation = self.rectify)


        # Layer 4: Logistic regression layer
        self.layer4 = LogisticRegression(input = self.dropout(self.layer3.output,p=0.2),
                                         n_in  = num_kernels[2] * self.edge2 * self.edge2,
                                         n_out = output_window_shape[0]*output_window_shape[1],
                                         out_window_shape = output_window_shape)
        
        # Define list of parameters
        convparams = self.layer2.params + self.layer1.params + self.layer0.params
        hiddenparams = self.layer4.params + self.layer3.params
        self.params = convparams + hiddenparams 