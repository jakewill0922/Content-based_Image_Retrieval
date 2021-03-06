from scipy.cluster.vq import *
from PCV.localdescriptors import sift
from numpy import *


class Vocabulary(object):
    def __init__(self, name):
        self.name = name
        self.voc = []
        self.idf = []
        self.trainingdata = []
        self.nbr_words = 0

    def train(self, featurefiles, k=100, subsampling=10):
        nbr_images = len(featurefiles)

        # read the features from files
        descr = []
        descr.append(sift.read_features_from_file(featurefiles[0])[1])
        descriptors = descr[0]
        for i in arange(1, nbr_images):
            descr.append(sift.read_features_from_file(featurefiles[i])[1])
            descriptors = vstack((descriptors, descr[i]))

        # modules-means: last number determines number of runs
        self.voc, distortion = kmeans(descriptors[::subsampling, :], k, 1)

        self.nbr_words = self.voc.shape[0]

        # go through all training images and project on vocabulary
        imwords = zeros((nbr_images, self.nbr_words))
        for i in range(nbr_images):
            imwords[i] = self.project(descr[i])

        nbr_occurences = sum((imwords > 0) * 1, axis=0)

        self.idf = log((1.0 * nbr_images) / (1.0 * nbr_occurences + 1))
        self.trainingdata = featurefiles

    def project(self, descriptors):

        # histogam of image words
        imhist = zeros((self.nbr_words))
        words, distance = vq(descriptors, self.voc)
        for w in words:
            imhist[w] += 1

        return imhist

