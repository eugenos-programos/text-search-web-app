
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class Metrics:
    def __init__(self, foundRelevant, foundNotRelevant, notFoundRelevant, notFoundNotRelevant):
        self.tp = foundRelevant
        self.fp = notFoundRelevant
        self.tn = foundNotRelevant
        self.fn = notFoundNotRelevant

    def getRecall(self):
        return self.tp / (self.tp + self.tn)

    def getPrecision(self):
        return self.tp / (self.tp + self.fp)

    def getAccuracy(self):
        return (self.tp + self.fn) / (self.tp + self.fp + self.tn + self.fn)

    def getError(self):
        return (self.fp + self.tn) / (self.tp + self.fp + self.tn + self.fn)

    def getF_measure(self):
        return 2 / (1 / self.getPrecision() + 1 / self.getRecall())

    def getAveragePrecision(self, k, positions):
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
        recall_levels = np.arange(0, 1.1, 0.1)
        interpolated_precisions = []

        for recall_level in recall_levels:
            recall_threshold = int(recall_level * num_relevant_docs)
            relevant_results = ranked_relevance[:recall_threshold]
            precision = sum(relevant_results) / (
                        recall_threshold + 1e-8) 
            interpolated_precisions.append(precision)

        return interpolated_precisions
