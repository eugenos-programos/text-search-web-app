
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class Metrics:
    def __init__(self, foundRelevant, foundNotRelevant, notFoundRelevant, notFoundNotRelevant):
        self.a = foundRelevant
        self.b = notFoundRelevant
        self.c = foundNotRelevant
        self.d = notFoundNotRelevant

    def getRecall(self):
        return self.a / (self.a + self.c)

    def getPrecision(self):
        return self.a / (self.a + self.b)

    def getAccuracy(self):
        return (self.a + self.d) / (self.a + self.b + self.c + self.d)

    def getError(self):
        return (self.b + self.c) / (self.a + self.b + self.c + self.d)

    def getF_measure(self):
        return 2 / (1 / self.getPrecision() + 1 / self.getRecall())

    def getAveragePrecision(self, k, positions):
        """
        Вычисляет среднюю точность (average precision).

        :param k: Количество релевантных документов
        :param positions: Список позиций, на которых релевантные документы были найдены
        :return: Значение средней точности
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
        Рассчитывает интерполированные значения точности для заданных уровней полноты.

        :param num_relevant_docs: Количество релевантных документов в коллекции
        :param ranked_relevance: Список булевых значений, где True означает, что документ релевантен
        :return: Список интерполированных значений точности
        """
        recall_levels = np.arange(0, 1.1, 0.1)  # Уровни полноты от 0 до 1 с шагом 0.1
        interpolated_precisions = []

        for recall_level in recall_levels:
            recall_threshold = int(recall_level * num_relevant_docs)
            relevant_results = ranked_relevance[:recall_threshold]
            precision = sum(relevant_results) / (
                        recall_threshold + 1e-8)  # Добавляем 1e-8 для избежания деления на ноль
            interpolated_precisions.append(precision)

        return interpolated_precisions
