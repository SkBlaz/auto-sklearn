import unittest

from sklearn.linear_model import RidgeClassifier
from ParamSklearn.components.preprocessing.kernel_pca import \
    KernelPCA
from ParamSklearn.util import _test_preprocessing, PreprocessingTestCase, \
    get_dataset
import sklearn.metrics


class KernelPCAComponentTest(PreprocessingTestCase):
    def test_default_configuration(self):
        transformation, original = _test_preprocessing(KernelPCA)
        self.assertEqual(transformation.shape[0], original.shape[0])
        self.assertFalse((transformation == 0).all())

    def test_default_configuration_classify(self):
        for i in range(5):
            X_train, Y_train, X_test, Y_test = get_dataset(dataset='digits',
                                                           make_sparse=False)
            configuration_space = KernelPCA.get_hyperparameter_search_space()
            default = configuration_space.get_default_configuration()
            preprocessor = KernelPCA(random_state=1,
                                   **{
                                       hp.hyperparameter.name: hp.value
                                       for hp in
                                       default.values.values()})
            preprocessor.fit(X_train, Y_train)
            X_train_trans = preprocessor.transform(X_train)
            X_test_trans = preprocessor.transform(X_test)

            # fit a classifier on top
            classifier = RidgeClassifier()
            predictor = classifier.fit(X_train_trans, Y_train)
            predictions = predictor.predict(X_test_trans)
            accuracy = sklearn.metrics.accuracy_score(predictions, Y_test)
            self.assertAlmostEqual(accuracy, 0.096539162112932606)

    @unittest.skip("Always returns float64")
    def test_preprocessing_dtype(self):
        super(KernelPCAComponentTest,
              self)._test_preprocessing_dtype(KernelPCA)

