# The class can be used to compute probabilities 
# e.g., p(h=5), probability of getting five heads when flipping a coin 10 times 
import random

class FlipCoin(object):
    """A class for coin flipping experiments"""
    def __init__(self, n):
        """n: number of flips"""
        self.n = n
        
    def outcomeSpace(self):
        """
        return the size of outcome space
        if self.n == 1, the function returns 2
        if self.n == 2, the function returns 4
        and so on
        """
        return 2**self.n
        

    def simulateOne(self):
        """
        a function that returns a simulation result as a list
        for example, if self.n = 2, the results can be any of 
        ["head", "tail"], ["tail", "head"], ["head", "head"], ["tail", "tail"]
        """
        #Implement me
         
        def recursive(n):
            
            if n <= 1:
                return [['head'],['tail']]
            else:
                l = recursive(n-1)
                l = l+ [item.copy() for item in l] 
                half = int(len(l)/2)
                for item in l[half:]:
                    item.append('head')
                for item in l[:half]:
                    item.append('tail')
                 
                return l
        return random.choice(recursive(self.n))   

             
        
    def simulation2Head(self):
        """
        a function that returns the number of heads in one experiment 
        (i.e. flipping a coin self.n times); for example, if self.n = 2, 
        the result can be either 0 (for 0 heads), 1, or 2
        """
        #Implement me
        l = self.simulateOne()

        return sum(1 for x in l if x=='head')
    def simulation2Prob(self, m = 1000):
        """
        estimate the probabilities of have 0, 1, ..., self.n heads, respectively, by simulation;
        m is the number of experiments
        the funtion returns [p(h=0), p(h=1), ... p(h=n)], 
        the probabilities of having 0 head, 1 head, ..self.n heads, as a list
        since this is a simulation, results may vary among different runs
        """
     
       
        head_counts = [0] * (self.n + 1)
            
        for i in range(m):
            simulation = random.choices(['head','tail'], k=self.n)
            
            count = sum(1 for j in simulation if j == 'head')
            
            head_counts[count] += 1
        f_array= [vals / m for vals in head_counts]
        print('array', head_counts)
        print('f_array: ', f_array)
        return f_array
    
    def count2Prob(self):
        """
        A function that computes the exact probabilities of having 0 h, 1 h, ...
        """
        #error
        outcome_space = self.outcomeSpace()
        
        array = [x/outcome_space for x in self.countHeads4All(self.n)]
        print('count2prob: ',array)
        return array
    def countHeads4All(self, n):
        """
        A function that counts the number of outcomes with 0, 1, ..., self.n heads
        after flipping n (the input) coins using recursion; 
        cuntHeads4All() is needed by count2Prob() to compute the exact probabilities.
        output: number of outcomes with 0, 1, ..., n heads, respectively, in a list
        """
        #Implement me
        def recursive(n):
            if n <= 1:
                return [['head'],['tail']]
            else:
                l = recursive(n-1)
                l = l+ [item.copy() for item in l] 
                half = int(len(l)/2)
                for item in l[half:]:
                    item.append('head')
                for item in l[:half]:
                    item.append('tail')
               
                return l
        l = recursive(self.n)
        og_selfn = self.n
        array = []
        outcome_space = self.outcomeSpace()
        array.extend([0]*int(outcome_space+1))
         
        for item in l:
            count = sum(1 for i in item if i=='head')
             
            array[count] += 1
        self.n = og_selfn
        for i in reversed(range(len(array))):
            if array[i] != 0:
                break

 
        array = array[:i + 1]
        return array

if __name__ == "__main__":
    
     
    """  
    n, h = 3, 1 #flip 3 coins & get 1 head

    fp = FlipCoin(n)
    fp.simulateOne()


    s = fp.outcomeSpace() # s = 8 
    c = fp.countHeads4All(n) # c = [1, 3, 3, 1]
    p1_a = fp.count2Prob()
    p1 = p1_a[h] #p1 = 0.375
    p2_a = fp.simulation2Prob()
    p2 = p2_a[h] #p2 is close to 0.375 
    p2_a = fp.simulation2Prob()
    print('p2:', p2)"""