import math


class SobelFilter:

    def __init__(self):
        self.gx_kernel = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]

        self.gy_kernel = [
            [1,  2,  1],
            [0,  0,  0],
            [-1, -2, -1]
        ]

        self.kernel_size = 3
        self.radius = 1  

    def apply(self, data):
        h = len(data)
        w = len(data[0])

        new_data = self._create_empty_image(w, h)

        for y in range(h):
            for x in range(w):
                gx = self._convolve_at_pixel(data, x, y, self.gx_kernel)
                gy = self._convolve_at_pixel(data, x, y, self.gy_kernel)

                magnitude = self._gradient_magnitude(gx, gy)
                new_data[y][x] = self._clamp_value(magnitude)

        return new_data


    def _create_empty_image(self, w, h):
        return [[0 for _ in range(w)] for _ in range(h)]

    def _convolve_at_pixel(self, data, x, y, kernel):

        h = len(data)
        w = len(data[0])
        total = 0

        for ky in range(-self.radius, self.radius + 1):
            for kx in range(-self.radius, self.radius + 1):
                nx, ny = x + kx, y + ky
                nx, ny = self._clamp_coords(nx, ny, w, h)

                pixel = data[ny][nx]
                weight = kernel[ky + self.radius][kx + self.radius]
                total += pixel * weight

        return total

    def _clamp_coords(self, x, y, w, h):
        cx = max(0, min(x, w - 1))
        cy = max(0, min(y, h - 1))
        return cx, cy

    def _gradient_magnitude(self, gx, gy):
        return math.sqrt(gx * gx + gy * gy)

    def _clamp_value(self, v):
        if v < 0:
            return 0
        if v > 255:
            return 255
        return int(v)
