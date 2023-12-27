import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('agg')

class Metrics:
    """
    Class for evaluating information retrieval metrics.

    Attributes:
        tp (int): Number of true positives (relevant documents correctly identified).
        fp (int): Number of false positives (non-relevant documents incorrectly identified as relevant).
        tn (int): Number of true negatives (non-relevant documents correctly identified).
        fn (int): Number of false negatives (relevant documents incorrectly identified as non-relevant).
    """

    def __init__(self, foundRelevant, foundNotRelevant, notFoundRelevant, notFoundNotRelevant):
        """
        Initialize Metrics object.

        Args:
            foundRelevant (int): Number of relevant documents correctly identified.
            foundNotRelevant (int): Number of non-relevant documents correctly identified.
            notFoundRelevant (int): Number of relevant documents incorrectly identified as non-relevant.
            notFoundNotRelevant (int): Number of non-relevant documents incorrectly identified as relevant.
        """
        self.tp = foundRelevant
        self.fp = notFoundRelevant
        self.tn = foundNotRelevant
        self.fn = notFoundNotRelevant

    def getRecall(self):
        """
        Calculate recall.

        Returns:
            float: Recall value.
        """
        return self.tp / (self.tp + self.tn)

    def getPrecision(self):
        """
        Calculate precision.

        Returns:
            float: Precision value.
        """
        return self.tp / (self.tp + self.fp)

    def getAccuracy(self):
        """
        Calculate accuracy.

        Returns:
            float: Accuracy value.
        """
        return (self.tp + self.fn) / (self.tp + self.fp + self.tn + self.fn)

    def getError(self):
        """
        Calculate error.

        Returns:
            float: Error value.
        """
        return (self.fp + self.tn) / (self.tp + self.fp + self.tn + self.fn)

    def getF_measure(self):
        """
        Calculate F-measure.

        Returns:
            float: F-measure value.
        """
        return 2 / (1 / self.getPrecision() + 1 / self.getRecall())

    def getAveragePrecision(self, k, positions):
        """
        Calculate average precision.

        Args:
            k (int): Number of documents to consider.
            positions (list): List of relevant document positions.

        Returns:
            float: Average precision value.
        """
        total_precision = 0.0
        num_relevant_docs_found = 0

        for i in range(k):
            if i in positions:
                num_relevant_docs_found += 1
                total_precision += num_relevant_docs_found / (i + 1)

        if num_relevant_docs_found == 0:
            return 0.0

        return total_precision / num_relevant_docs_found

    def calculateInterpolatedPrecision(self, num_relevant_docs, ranked_relevance):
        """
        Calculate interpolated precision.

        Args:
            num_relevant_docs (int): Number of relevant documents.
            ranked_relevance (list): List of relevance scores for ranked documents.

        Returns:
            list: Interpolated precision values.
        """
        recall_levels = np.arange(0, 1.1, 0.1)
        interpolated_precisions = []

        for recall_level in recall_levels:
            recall_threshold = int(recall_level * num_relevant_docs)
            relevant_results = ranked_relevance[:recall_threshold]
            precision = sum(relevant_results) / (recall_threshold + 1e-8)
            interpolated_precisions.append(precision)

        return interpolated_precisions
