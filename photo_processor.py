import numpy as np
from sklearn.cluster import KMeans
from matplotlib.colors import to_hex


class ColorProcessor:
    def __init__(self, img):
        img_arr = np.asarray(img)
        if img_arr.shape[2] == 3:
            color_arr = np.reshape(img_arr, (-1, 3))
        elif img_arr.shape[2] == 4:
            color_arr = np.reshape(img_arr, (-1, 4))
        self.kmeans = KMeans(n_clusters=10, n_init='auto').fit(color_arr)
        self.no_of_pixels = self.kmeans.labels_.shape[0]

    def color_dist(self):
        color_values, color_counts = np.unique(self.kmeans.labels_, return_counts=True)

        colors = (self.kmeans.cluster_centers_.round(decimals=0)).astype(int)
        self.colors = colors.tolist()
        color_count = dict(zip(color_values, color_counts))
        color_pct = {key: round(color_count[key]/self.no_of_pixels*100, 2) for key in color_count}
        return self.colors, color_pct

    def hex_colors(self):
        hex_colors = []
        for color in self.colors:
            rgb_color = [value/255 for value in color]
            hex_color = to_hex(rgb_color)
            hex_colors.append(hex_color)
        return hex_colors

    def color_brightness(self):
        brightness = []
        for color in self.colors:
            luma = 0.212*color[0] + 0.701*color[1] + 0.087+color[2]
            brightness.append(luma)
        print(brightness)
        return brightness
