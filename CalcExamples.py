

# ThresholdOr computation
# n - number of drones and number of target picture slides
# l - number of target image pixels
def ThresholdOr(X, t):
    for k,j in [0..l]:
        X_kj = 0
        for i in [0..n]:
            X_kj += X[i][k,j]     
        if X_kj > t:
            Y[k,j] = 1
        else:
            Y[k,j] = 0
    return Y

# Shamir with target image encoding
# Compare CA and TA pixels
# n - number of drones and number of target picture slides
# l - number of target image pixels
def CompareImagesMPC(C, TA):
    CA = EncodeImagetoArray(C)
    for k,j in [0..l]:
        X_kj = 0
        if CA[k,j] == TA[k,j]:
            Y[k,j] = 1
        else:
            Y[k,j] = 0
    return Y

# Plain Shamir SS with MPC
# Compare C and T pixels
# n - number of drones and number of target picture slides
# l - number of target image pixels
def CompareImagesMPC(C, T):
    for k,j in [0..l]:
        X_kj = 0
        if C[k,j] == T[k,j]:
            Y[k,j] = 1
        else:
            Y[k,j] = 0
    return Y
