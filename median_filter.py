class MedianFilter:

    def __init__(self, kernel_size=3):

        if kernel_size % 2 == 0:
            raise ValueError("kernel_size musi być nieparzysty")
        self.kernel_size = kernel_size
        self.radius = kernel_size // 2

    def apply(self, data):
        h = len(data)
        w = len(data[0])

        new_data = self._create_empty_image(w, h)

        for y in range(h):
            for x in range(w):
                new_data[y][x] = self._median_for_pixel(data, x, y)

        return new_data


    def _create_empty_image(self, w, h):
        return [[0 for _ in range(w)] for _ in range(h)]

    def _median_for_pixel(self, data, x, y):
        neighbors = self._get_neighbors(data, x, y)
        return self._compute_median(neighbors)

    def _get_neighbors(self, data, x, y):
        h = len(data)
        w = len(data[0])
        values = []

        for dy in range(-self.radius, self.radius + 1):
            for dx in range(-self.radius, self.radius + 1):
                nx, ny = x + dx, y + dy
                nx, ny = self._clamp_coords(nx, ny, w, h)
                values.append(data[ny][nx])

        return values

    def _clamp_coords(self, x, y, w, h):
        cx = max(0, min(x, w - 1))
        cy = max(0, min(y, h - 1))
        return cx, cy

    def _compute_median(self, values):
        sorted_vals = self._sort_values(values)
        mid = len(sorted_vals) // 2
        return sorted_vals[mid]

    def _sort_values(self, values):
        return sorted(values)
