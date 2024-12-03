# Place your imports here
import numpy as np
import pandas as pd
import random 

class MiniData(object):
    """a class for basic data operation"""
    def toyList(self, n):
        result = []
        for i in range(n):
            if i == 0:
                result.append(1)
            else:
                result.append(result[i-1]+i)
        """return a python list of n numbers in this pattern: 1, 2, 4, 7, 11, 16, ..."""
        #Implement me
        return result

    def toyVector(self):
        """create a vector containing the following numbers: 
        and return it as a numpy array"""
        vector = (1,4,5,7,9,10) 
        vector = np.array(vector)
        #Implement me
        return vector

    def toyMatrix(self, n, m):
        """
        generate a toy matrix of n by m integers in the range of [0, 100] and return the matrix as a numpy array of nxm.
        use random module to generate the integers randomly 
        """ 
        #toymatrix = np.array([np.random.randint(0, 100, size=(n,m))])
        toymatrix = np.empty((n,m))
        for x in range(n):
            for y in range(m):
                toymatrix[x][y] = random.randint(0, 100)
                
        #Implement me
        return toymatrix

    def toyDataframe(self):
        """
        create a toy dataset and represent it using Pandas dataframe, return the dataframe
        it contains 10 people (objects) with three attributes, 'Refund', 'Marital Status' and 'Taxable Income'
        again using random to generate values for these attributes, 
            'Refund' can be 'Yes' or 'No', 
            'Marital Status' can be 'Married', 'Single', or 'Divorced'
            'Taxable Income' is an integer in the range of [50, 500] (50 represents 50k etc)
        """ 
        #toy_dataset = self.toyMatrix(10, 3)
        refund = ["Yes", "No"]
        marital_status = ["Married", "Single", "Divorced"]
        #Implement me
        df = pd.DataFrame({
            'Refund': pd.Categorical(random.choices(refund, k=10), categories=refund, ordered=False),
            'Marital Status': pd.Categorical(random.choices(marital_status, k=10),categories=marital_status, ordered=False),
            'Taxable Income': pd.Series(np.random.randint(0, 500, size=(10))),
        })
            
            
        return df

class Billy(object):
    def __init__(self):
        self.better = 1.5

    def majority(self, nums):
        """
        the input nums is a list containing the speedup numbers; 
        if more than half of the numbers in nums are equal to or greater than self.better
        the algorithm is considered to be faster so this function returns 'faster', otherwise 'no improvement'
        """
        counter = np.sum(np.array(nums) >= self.better)
        
        if counter >= len(nums)/ 2:
            return 'faster'
        else:
            return 'no improvement'

        #Implement me
        
    
    def meanBased(self, nums, mean="arithmetic"):
        if mean == "geometric":
            mean = np.prod(nums)**(1/len(nums))
        else:

            mean = np.mean(nums)

        if mean >= self.better:
            return 'faster'
        else:
             return 'no improvement'
        
        """
        this function implements a different approach for evaluating the speedups. 
        if the mean of the speedups is equal to or great than self.better, 
        the function returns 'faster', otherwise, 'no improvement'
        mean can be either 'arithmetic' or 'geometric', which specifies the approach for computing the mean
        """
        #Implement me
        

if __name__ == '__main__':
    md = MiniData()
    #print(md.toyDataframe())
    #print(md.toyList(12))
    #print(md.toyMatrix(4,5))
    #print(md.toyDataframe())
    t = Billy()
    nums = [2.0, 0.5, 1.0, 2.0, 100]
    #print(t.majority(nums)) #faster
    #print(t.meanBased(nums)) #faster
    #print(t.meanBased(nums, mean="geometric")) #faster

