import numpy as np
import pytest
import tensorflow as tf

import keras
from keras.src import backend
from keras.src import testing


@pytest.mark.skipif(
    backend.backend() != "tensorflow",
    reason="The nestedstructure test can only run with TF backend.",
)
def dict_input_fn(inputs):
    x = inputs["x"][:, 0]
    y = inputs["y"] + 1
    return {"x": x, "y": y}


def list_input_fn(inputs):
    return [x**2 for x in inputs]


class NestedTest(testing.TestCase):
    def setUp(self):
        self.xs = {
            "x": tf.convert_to_tensor(
                np.random.rand(4, 100, 3), dtype=tf.float32
            ),
            "y": tf.convert_to_tensor(
                np.random.randint(0, 10, size=(4, 1)), dtype=tf.int32
            ),
        }
        self.xs1 = [
            tf.convert_to_tensor(np.random.rand(4, 100, 3), dtype=tf.float32),
            tf.convert_to_tensor(
                np.random.randint(0, 10, size=(4, 1)), dtype=tf.int32
            ),
        ]

    def test_dict_input_fn_outputs(self):
        ys = keras.ops.map(dict_input_fn, self.xs)
        self.assertEqual(ys["x"].shape, (4, 100))
        self.assertEqual(
            keras.ops.convert_to_numpy(ys["y"]).all(),
            keras.ops.convert_to_numpy(self.xs["y"] + 1).all(),
        )

    def test_list_input_fn_outputs(self):
        ys = keras.ops.map(list_input_fn, self.xs1)
        for i, (x, y) in enumerate(zip(self.xs1, ys)):
            self.assertEqual(
                (keras.ops.convert_to_numpy(y)).all(),
                (keras.ops.convert_to_numpy(x) ** 2).all(),
            )
