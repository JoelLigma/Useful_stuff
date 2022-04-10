import math

def confidence_interval(sample_error, zn, n):
    """
    This function computes the confidence interval for the true error.
    """
    lower_bound = sample_error - zn * math.sqrt(((sample_error * (1 - sample_error)) / n))
    upper_bound = sample_error + zn * math.sqrt(((sample_error * (1 - sample_error)) / n))
    return f"Lower bound: {round(lower_bound, 3)}, Upper bound: {round(upper_bound, 3)}"
