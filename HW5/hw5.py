import math
def impurity(d, method="gini"):
     
    prob_d = [i for i in d.values()]
    if method == 'gini':
        for i in range(len(prob_d)):
            prob_d[i] = prob_d[i] ** 2
        return 1 - sum(prob_d)
    
    elif method == 'entropy':
        for i in range(len(prob_d)):
            if prob_d[i] > 0:
                prob_d[i] = prob_d[i] * math.log2(prob_d[i])
            else:
                prob_d[i] = 0
        return -sum(prob_d)

         
         
    elif method == 'error':
        return 1 - max(prob_d)

"""return the impurity score for a training set with given class distribution d
input: d: dictionary of class distribution in counts or frequency
input: method, can be "gini", "entropy", or "error"
output: impurity score
example 1: impurity({"Yes":0.5, "No":0.5}, method="gini") returns 0.5
example 2: impurity({"ClassI":45, "ClassII":45}, method="gini") returns 0.5
example 3: impurity({"A":0.25, "B":0.25, "C":0.25, "D":0.25}, method="entropy"
returns 2.0
note: for the purpose of defining/computing entropy, 0 log2(0) is defined to be
0.
"""
#Implement me
if __name__ == "__main__":
    data = [{"Yes":0.5, "No":0.5}, {"ClassI":45, "ClassII":45}, {"A":0.25,
    "B":0.25, "C":0.25, "D":0.25}]
    method = ["gini", "entropy", "error"]
    for d, m in zip(data, method):
        print(impurity(d, m))
