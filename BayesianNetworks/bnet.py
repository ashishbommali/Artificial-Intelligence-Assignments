import numpy as np
import sys

#CLASS FOR BAYESIAN NETWORK 
class BayesNets:
    def __init__(self, data_file):
        self.data = data_file
        self.p_B = np.zeros((2,))
        self.p_G = np.zeros((2, 2))
        self.p_C = np.zeros((2))
        self.p_F = np.zeros((2, 2, 2))
        self.calculate_probabilities()

    # Count the occurrences of each variable given its parents
    def calculate_probabilities(self):
        # Count occurrences of each variable value
        counts = np.bincount(self.data.ravel(), minlength=8).reshape(2, 2, 2)

        # Compute marginal probabilities
        self.p_B = counts[:, 0, 0] / counts.sum()
        self.p_G = counts[:, :, 0] / counts[:, :, :2].sum(axis=2, keepdims=True)
        self.p_C = counts[0, :, 0] / counts[0].sum()
        self.p_F = np.stack([
            counts[:, :, 0] / counts[:, :, :2].sum(axis=2, keepdims=True),
            counts[:, :, 1] / counts[:, :, 1:].sum(axis=2, keepdims=True)
        ], axis=2)

        # Print the probability matrices
        print("Probability matrices: ")
        print("P(B):")
        print(self.p_B)
        print("P(G|B):")
        print(self.p_G)
        print("P(C):")
        print(self.p_C)
        print("P(F|G,C):")
        print(self.p_F)

    def calculateJPD(self,B,G,C,F):
        # Calculate the joint probability using the conditional probabilities
        p_joint = self.p_B[B] * self.p_G[B][G] * self.p_C[C] * self.p_F[G][C][F]

        print(self.p_B[B] ,"*", self.p_G[B][G], "*", self.p_C[C], "*", self.p_F[G][C][F])

        # Print the result
        print("JPD P(B={}, G={}, C={}, F={}) = {:.17f}".format(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], p_joint))

#DRIVER CODE 
if __name__ == '__main__':
    # Read the training data from a file
    data = np.loadtxt(sys.argv[1])
    bnet = BayesNets(data)

    if len(sys.argv)<=1:
        bnet.calculate_probabilities()
    elif len(sys.argv)>2:
        args = sys.argv[2:]
        variables = []
        evidence = []

        try:
            i = args.index("given")
            variables = args[:i]
            evidence = args[i + 1:]
        except ValueError:
            variables = args

        if len(evidence)==0 and len(variables)==4:
            # Get the command line arguments
            B = 1 if sys.argv[2] == "Bt" else 0
            G = 1 if sys.argv[3] == "Gt" else 0
            C = 1 if sys.argv[4] == "Ct" else 0
            F = 1 if sys.argv[5] == "Ft" else 0
            bnet.calculate_probabilities()
            bnet.calculateJPD(B,G,C,F)
        elif len(evidence)==0 and len(variables)<4:
            print("calculate prob using inference by enumeration:")
            
        else:
            print("calculate prob using given evidence by enumeration:")
            print("Variables:", variables)
            print("Given evidence:", evidence)
            
