import numpy as np
import scipy as sp


class SoundEnhansement:
    """
    Class that contains different sound enhansement methods.
    """

    @staticmethod
    def process(data: np.ndarray):
        return
    
    @staticmethod
    def lib_wiener(data: np.ndarray):
        """
        Applies the Wiener filter to the given data.

        Args:
            data (np.ndarray): The input data to be filtered.

        Returns:
            np.ndarray: The filtered data.
        """

        def process_channel(data: np.ndarray):
            """
            Processes a single channel of data.

            Args:
                data (np.ndarray): The input data for a single channel.

            Returns:
                np.ndarray: The processed data for the channel.
            """

            wiener_n = 10

            R = np.correlate(data, data, mode='full')
            R = R[(R.size // 2 - wiener_n // 2):(R.size // 2 + wiener_n // 2 + 1)]
            R_matrix = np.array([R[i:i+wiener_n] for i in range(len(R) - wiener_n + 1)])

            P = sp.signal.correlate(data, data, mode='full')
            P = P[P.size//2:P.size//2+wiener_n]

            h = np.linalg.solve(R_matrix, P)

            return sp.signal.lfilter(h, 1.0, data)

        channels = data.shape[1]
        filtered_data = None

        # For Stereo Audio
        if channels == 2:
            filtered_data = np.transpose([process_channel(ch) for ch in np.transpose(data)])

        # For Mono Audio
        else:
            filtered_data = process_channel(data)

        
        return filtered_data
