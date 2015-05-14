import numpy as np
import sys

def post_process(x_train,y_train,output,y,table,img_shape,in_window_shape,out_window_shape,classifier,n_train_examples = 100):
    
    diff = in_window_shape-out_window_shape

    y      = y.reshape(y.shape[0],out_window_shape,out_window_shape)  
    output = output.reshape(output.shape[0],out_window_shape,out_window_shape)         
        
    nr_images    = np.max(table[:,0]) + 1 

    y_whole      = np.zeros((nr_images, img_shape[0]-diff, img_shape[0]-diff))
    output_whole = np.zeros((nr_images, img_shape[0]-diff, img_shape[0]-diff))
    count        = np.zeros((nr_images, img_shape[0]-diff, img_shape[0]-diff))

    for i in xrange(table.shape[0]):       
        y_whole[table[i,0],(table[i,1]):(table[i,1]+out_window_shape),(table[i,2]):(table[i,2] + out_window_shape)]      += y[i]      
        output_whole[table[i,0],(table[i,1]):(table[i,1]+out_window_shape),(table[i,2]):(table[i,2] + out_window_shape)] +=  output[i] 
        count[table[i,0],(table[i,1]):(table[i,1]+out_window_shape),(table[i,2]):(table[i,2] + out_window_shape)] += np.ones((out_window_shape,out_window_shape))                                              

    count = count.astype(np.float32)

    y_whole      /= count
    output_whole /= count

    return output_whole, y_whole
    
if __name__ == "__main__":
    post_process()
