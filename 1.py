{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled3.ipynb",
      "provenance": [],
      "authorship_tag": "ABX9TyNCYbnys3NGF1oAsc5wnHhs",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Erenere/ICGrLFqa1TiymKPG/blob/main/1.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "HMNMVym4Akfz",
        "outputId": "20a6ad5d-c423-4f8a-df8f-5ad161d3e790"
      },
      "source": [
        "# -*- coding: utf-8 -*-\n",
        "\n",
        "!pip install -q sklearn # if needed\n",
        "\n",
        "# Commented out IPython magic to ensure Python compatibility.\n",
        "# %tensorflow_version 2.x\n",
        "\n",
        "from __future__ import absolute_import, division, print_function, unicode_literals\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "from IPython.display import clear_output\n",
        "from six.moves import urllib\n",
        "from sklearn.model_selection import train_test_split\n",
        "import tensorflow.compat.v2.feature_column as fc\n",
        "import tensorflow as tf\n",
        "from tensorflow.keras.layers.experimental import preprocessing\n",
        "from tensorflow.keras import layers\n",
        "from tensorflow import keras\n",
        "\n",
        "df=pd.read_csv(\"/content/ACME-HappinessSurvey2020.csv\")\n",
        "\n",
        "dftrain = df.copy()\n",
        "dfeval = df.copy()\n",
        "\n",
        "y_train = dftrain.pop('Y')\n",
        "y_eval = dfeval.pop('Y')\n",
        "for y in y_train:\n",
        "  y=int(y)\n",
        "for y in y_eval:\n",
        "  y=int(y)\n",
        "# dftrain.head()\n",
        "\n",
        "def build_and_compile_model(norm):\n",
        "  model = keras.Sequential([\n",
        "      norm,\n",
        "      layers.Dense(64, activation='relu'),\n",
        "      layers.Dense(64, activation='relu'),\n",
        "      layers.Dense(1)\n",
        "  ])\n",
        "\n",
        "  model.compile(loss='binary_crossentropy',\n",
        "                optimizer=tf.keras.optimizers.Adam(0.001),\n",
        "                metrics=[\"accuracy\"])\n",
        "  return model\n",
        "\n",
        "normalizer = preprocessing.Normalization()\n",
        "normalizer.adapt(np.array(dftrain))\n",
        "\n",
        "dnn_model = build_and_compile_model(normalizer)\n",
        "#dnn_model.summary()\n",
        "\n",
        "# %%time\n",
        "history = dnn_model.fit(\n",
        "    dftrain, y_train,\n",
        "    validation_split=0.2,\n",
        "    verbose=0, epochs=100)\n",
        "\n",
        "test_results = {}\n",
        "test_results['dnn_model'] = dnn_model.evaluate(dfeval, y_eval, verbose=1)\n",
        "# test_results\n",
        "\n",
        "dnn_model.save('dnn_model')\n",
        "\n",
        "sample_size=126\n",
        "pred=dnn_model.predict_classes(dfeval[:sample_size])\n",
        "\n",
        "real=y_eval[:sample_size]\n",
        "score=0\n",
        "for i in range(sample_size):\n",
        "  if pred[i]==real[i]:\n",
        "    score+=1\n",
        "print(f'score: {score/sample_size}')"
      ],
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "4/4 [==============================] - 0s 3ms/step - loss: 1.0344 - accuracy: 0.8254\n",
            "INFO:tensorflow:Assets written to: dnn_model/assets\n",
            "score: 0.8253968253968254\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.7/dist-packages/tensorflow/python/keras/engine/sequential.py:455: UserWarning: `model.predict_classes()` is deprecated and will be removed after 2021-01-01. Please use instead:* `np.argmax(model.predict(x), axis=-1)`,   if your model does multi-class classification   (e.g. if it uses a `softmax` last-layer activation).* `(model.predict(x) > 0.5).astype(\"int32\")`,   if your model does binary classification   (e.g. if it uses a `sigmoid` last-layer activation).\n",
            "  warnings.warn('`model.predict_classes()` is deprecated and '\n"
          ],
          "name": "stderr"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "pP1U2mnCCXD0",
        "outputId": "9b0a14dc-138b-4806-9aff-50219b45c0d1"
      },
      "source": [
        "# pearson's correlation feature selection for numeric input and numeric output\n",
        "from sklearn.datasets import make_regression\n",
        "from sklearn.feature_selection import SelectKBest\n",
        "from sklearn.feature_selection import f_regression\n",
        "\n",
        "fs = SelectKBest(score_func=f_regression, k=1)\n",
        "# apply feature selection\n",
        "X_selected = fs.fit_transform(dftrain, y_train)\n",
        "print(X_selected)\n",
        "# Most important feature -> X1"
      ],
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[[3]\n",
            " [3]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [3]\n",
            " [5]\n",
            " [4]\n",
            " [4]\n",
            " [3]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [4]\n",
            " [3]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [4]\n",
            " [4]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [3]\n",
            " [3]\n",
            " [3]\n",
            " [3]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [3]\n",
            " [3]\n",
            " [4]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [3]\n",
            " [5]\n",
            " [5]\n",
            " [1]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [4]\n",
            " [3]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [4]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [3]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [3]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [3]\n",
            " [3]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [3]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [3]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [3]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [4]\n",
            " [5]\n",
            " [5]\n",
            " [5]\n",
            " [4]\n",
            " [5]]\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "PXE539GTLF9N",
        "outputId": "004a5fc7-aa91-44aa-d535-0efc7dfa306b"
      },
      "source": [
        "from sklearn.ensemble import ExtraTreesClassifier\n",
        "\n",
        "model = ExtraTreesClassifier(n_estimators=10)\n",
        "model.fit(dftrain, y_train)\n",
        "print(model.feature_importances_)\n",
        "# X1 is the most important, X2 and X3 have also high importance"
      ],
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[0.19411442 0.18979693 0.19306574 0.1576853  0.13934504 0.12599258]\n"
          ],
          "name": "stdout"
        }
      ]
    }
  ]
}