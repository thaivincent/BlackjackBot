import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import datasets, layers, models
import os

(training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data()
training_images, testing_images = training_images / 255 , testing_images / 255

class_names = [""]

