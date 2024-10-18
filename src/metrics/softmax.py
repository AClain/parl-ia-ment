import numpy as np


def softmax(x: np.ndarray[float]) -> float:
    """
    Compute the softmax of a given NumPy array of logprobs.

    Parameters:
    ----------
    x : np.ndarray[float]
        A NumPy array of floats representing logprobs.

    Returns:
    -------
    np.ndarray[float]
        A NumPy array containing the softmax probabilities for the input array of logprobs.
    """

    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
