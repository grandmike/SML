import numpy as np
import math
class ProbabilityModel:

    # Returns a single sample (independent of values returned on previous calls).
    # The returned value is an element of the model's sample space.
    def sample(self):
        return np.random.uniform()
    
    def pmf(self, n):
        return np.array([self.sample() for i in range(n)])


# The sample space of this probability model is the set of real numbers, and
# the probability measure is defined by the density function 
# p(x) = 1/(sigma * (2*pi)^(1/2)) * exp(-(x-mu)^2/2*sigma^2)
class UnivariateNormal(ProbabilityModel):
    
    # Initializes a univariate normal probability model object
    # parameterized by mu and (a positive) sigma
    def __init__(self,mu,sigma):
        self.mu = mu
        self.sigma = sigma

    def sample(self):
        u1 = np.random.uniform()
        u2 = np.random.uniform()
        x = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        return x * self.sigma + self.mu
        

# The sample space of this probability model is the set of D dimensional real
# column vectors (modeled as numpy.array of size D x 1), and the probability 
# measure is defined by the density function 
# p(x) = 1/(det(Sigma)^(1/2) * (2*pi)^(D/2)) * exp( -(1/2) * (x-mu)^T * Sigma^-1 * (x-mu) )
class MultiVariateNormal(ProbabilityModel):
    
    # Initializes a multivariate normal probability model object 
    # parameterized by Mu (numpy.array of size D x 1) expectation vector 
    # and symmetric positive definite covariance Sigma (numpy.array of size D x D)
    def __init__(self,Mu,Sigma):
        self.Mu = Mu
        self.Sigma = Sigma

    def sample(self, low=None, high=None, size=None):
        Z = []
        L = np.linalg.cholesky(self.Sigma)
        for i in range(0, self.Mu.size):
            Z.append(UnivariateNormal(0, 1).sample())
        return self.Mu + np.dot(L, Z)

# The sample space of this probability model is the finite discrete set {0..k-1}, and 
# the probability measure is defined by the atomic probabilities 
# P(i) = ap[i]
class Categorical(ProbabilityModel):
    
    # Initializes a categorical (a.k.a. multinom, multinoulli, finite discrete) 
    # probability model object with distribution parameterized by the atomic probabilities vector
    # ap (numpy.array of size k).
    def __init__(self, ap):
        self.ap = ap
        self.sum = []
        t = 0
        for i in range(0, len(self.ap)):
            t += self.ap[i]
            self.sum.append(t)

    def sample(self):
        u = np.random.uniform(0,1)
        for i in range(0, len(self.sum)):
            if u < self.sum[i]:
                return i


# The sample space of this probability model is the union of the sample spaces of 
# the underlying probability models, and the probability measure is defined by 
# the atomic probability vector and the densities of the supplied probability models
# p(x) = sum ad[i] p_i(x)
class MixtureModel(ProbabilityModel):
    
    # Initializes a mixture-model object parameterized by the
    # atomic probabilities vector ap (numpy.array of size k) and by the tuple of 
    # probability models pm
    def __init__(self,ap,pm):
        self.ap = ap
        self.pm = pm

    def sample(self):
        categorical = Categorical(self.ap)
        return self.pm[categorical.sample()].sample()
