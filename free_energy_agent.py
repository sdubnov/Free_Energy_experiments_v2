#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 11:48:09 2018

@author: aidanrocke
"""

import tensorflow as tf
import numpy as np
import tensorflow_probability as tfp

class free_agent:
    
    def __init__(self,basic_needs,sess,success_probability):
        self.survival = tf.compat.v1.placeholder(tf.float32, [None, 1])
        self.sess = sess
        self.basic_needs = basic_needs
        self.strategy = self.decision_network()
        self.p = success_probability
        
    
    def init_weights(self,shape,var_name):
        """
            Xavier initialisation of neural networks
        """
        initializer = tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform")
        return tf.Variable(initializer(shape),name = var_name)
    
    def decision_network(self):
        """
        This function calculates a food policy which is optimal
        for the agent's homeostatic conditions. 
        
        input: survival policy
        output: food policy
        """
        
        with tf.compat.v1.variable_scope("decision"):
            
            tf.compat.v1.set_random_seed(42)
    
            w_h = self.init_weights([1,100],"w_h")
            w_h2 = self.init_weights([100,100],"w_h2")
            w_o = self.init_weights([100,24],"w_o")
            
            ### bias terms:
            bias_1 = self.init_weights([100],"bias_1")
            bias_2 = self.init_weights([100],"bias_2")
            bias_3 = self.init_weights([24],"bias_3")
                
            h = tf.nn.elu(tf.add(tf.matmul(self.survival, w_h),bias_1))
            h2 = tf.nn.elu(tf.add(tf.matmul(h, w_h2),bias_2))
            
        return tf.nn.sigmoid(tf.add(tf.matmul(h2, w_o),bias_3))
    
    def surprise(self):
        
        #get probability of success:
        success_vector = tf.convert_to_tensor(value=np.random.choice((0.0,1.0),size=24,p=(1-self.p,self.p)))
        total = tf.multiply(tf.cast(success_vector,tf.float32),self.strategy)
        
        ## define normal distribution:
        dist = tfp.distributions.Normal(self.basic_needs,1.0)
        
        print(total,dist.log_prob(total))
              
        return dist.log_prob(total)
