class BinarizeFilter:

    def __init__(self, threshold=128):
        self.threshold = threshold

    def apply(self, data):

        h = len(data)
        w = len(data[0])

        bin_data = self._create_empty_image(w, h)

        for y in range(h):
            for x in range(w):
                bin_data[y][x] = self._binarize_pixel(data[y][x])

        return bin_data


    def _create_empty_image(self, w, h):
        return [[0 for _ in range(w)] for _ in range(h)]

    def _binarize_pixel(self, v):
        return 255 if v >= self.threshold else 0
