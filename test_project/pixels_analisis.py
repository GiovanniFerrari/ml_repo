import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

from PIL import Image, ImageOps

colourImg = Image.open("images/" + sys.argv[1])
colourPixels = colourImg.convert("HSV")

import numpy as np
colourArray = np.array(colourPixels.getdata()).reshape(colourImg.size + (3,))
indicesArray = np.moveaxis(np.indices(colourImg.size), 0, 2)
allArray = np.dstack((indicesArray, colourArray)).reshape((-1, 5))

import pandas as pd
df = pd.DataFrame(allArray, columns=["y", "x", "red","green","blue"])

labeledImg = Image.open("images-selected/" + sys.argv[1])

grayArray = np.array(ImageOps.grayscale(labeledImg))

df["label"] = grayArray.flatten()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
threedee = plt.figure().gca(projection='3d')

df_negative = df[df["label"]==0]

df_positive = df[df["label"]==255]

threedee.scatter(df_positive["red"],df_positive["green"],df_positive["blue"], alpha=0.1,c="red")
threedee.scatter(df_negative["red"],df_negative["green"],df_negative["blue"], alpha=0.1,c="blue")

plt.show()
