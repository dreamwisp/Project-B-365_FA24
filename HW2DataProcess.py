import math

class DataProcessor(object):
    """
    a class for basic data operations & processing
    in the following functions, x and y are python lists representing data objects
    """
    def summary(self, x):
        """
        input: x, a python list

        output/return: a tuple of three numbers: mean, median, variance (using ddof = 1)
        for median, you will use a slow algorithm that first sorts the input list; 
        if the number of numbers in x is odd, the median is the middle one in the sorted list; 
        otherwise, the median is an average of the middle two numbers.
        """
        len_of_x = len(x)
         
        mean = sum(x)/len_of_x
         
         
        variance = sum((item-mean)**2 for item in x)/(len_of_x-1)
         
        sorted_x = sorted(x)
        m = int(len(x)/2)
        if len(x) % 2 == 0:
            
            median = (sorted_x[m] + sorted_x[m-1])/2
        else:
            median = sorted_x[m]

        
        #Implement me
        return (mean, median, variance)

    def dot(self, x, y):
        """
        input: python lists x and y
        output/return: dot product of x and y 
        """
        if len(x) != len(y):
        
            min_length = min(len(x),len(y))
            x = x[:min_length]
            y= y[:min_length]
         
        return sum(i*j for i,j in zip(x,y))
        #Implement me
         

    def cov(self, x, y):
        """
        input: python lists x and y
        output/return: covariance between x and y 
        use ddof = 1
        """
        if len(x) != len(y):
        
            min_length = min(len(x),len(y))
            x = x[:min_length]
            y= y[:min_length]
        ddof = 1
        
        mean_x = self.summary(x)[0]
        mean_y = self.summary(y)[0]
        sum_of = sum(((x_i-mean_x)*(y_i-mean_y)) for x_i, y_i in zip(x, y))
         
        return sum_of/(len(x)-ddof)
    def corr(self, x, y):
        """
        input: python lists x and y
        output/return: the Pearson correlation coefficient between x and y
        use cov() and summary() to complete this function
        """ 
        if len(x) != len(y):
        
            min_length = min(len(x),len(y))
            x = x[:min_length]
            y= y[:min_length]
         
        mean_x = self.summary(x)[0]
        mean_y = self.summary(y)[0]
        std_x = math.sqrt(sum((x_i - mean_x) ** 2 for x_i in x) / (len(x) - 1))
        std_y = math.sqrt(sum((y_i - mean_y) ** 2 for y_i in y) / (len(y) - 1))
        
        return self.cov(x,y)/(std_x*std_y)

    def SMC(self, x, y):
        """
        input: python lists x and y of 0 and 1s (representing binary vectors)
        output/return: simple match score
        """
        #Implement me
        matches = sum(1 for x_i, y_i in zip(x, y) if x_i==y_i)
        return matches/len(x)

    def Jaccard(self, x, y):
        """
        input: python lists x and y of 0 and 1s (representing binary vectors)
        output/return: Jaccard similarity 
        """
         
        intersection = sum(1 for i_x, i_y in zip(x,y) if i_x == 1 and i_y == 1)
        union = sum(1 for i_x, i_y in zip(x,y) if i_x==1 or i_y==1)
        jaccard_similarity = intersection/union
      
        return jaccard_similarity

    def Cosine(self, x, y):
        """
        input: python lists x and y of floats
        output/return: Cosine between x and y
        """
        dot_vectors = self.dot(x,y)
        A = sum(item ** 2 for item in x)**(1/2)
        B = sum(item ** 2 for item in y)**(1/2)
        return dot_vectors/(A*B)

    def Euclidean(self, x, y):
        """
        input: python lists x and y of floats
        output/return: Euclidean distance between x and y
        """
        euclidean = math.sqrt(sum((i_y - i_x)**2 for i_x, i_y in zip(x,y)))
            
        #Implement me
        return euclidean

if __name__ == '__main__':
    dp = DataProcessor()

    bx1 = [1, 1, 1, 1, 0, 0]
    by1 = [0, 0, 0, 0, 1, 1]
    #print(dp.Jaccard(bx1, by1))
