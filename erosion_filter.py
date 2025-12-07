class ErosionFilter:
    def __init__(self, struct_elem):
        self.struct_elem = struct_elem
        self.se_h = len(struct_elem)
        self.se_w = len(struct_elem[0])
        self.radius_y = self.se_h // 2
        self.radius_x = self.se_w // 2

    def apply(self, bin_data):
        h = len(bin_data)
        w = len(bin_data[0])

        new_data = self._create_empty_image(w, h)

        for y in range(h):
            for x in range(w):
                new_data[y][x] = self._erode_pixel(bin_data, x, y)

        return new_data

    def _create_empty_image(self, w, h):
        return [[0 for _ in range(w)] for _ in range(h)]

    def _erode_pixel(self, bin_data, x, y):
        neighbors = self._get_structured_neighbors(bin_data, x, y)

        for v in neighbors:
            if v == 0:
                return 0
        return 255

    def _get_structured_neighbors(self, bin_data, x, y):
        h = len(bin_data)
        w = len(bin_data[0])
        values = []

        for sy in range(self.se_h):
            for sx in range(self.se_w):
                if self.struct_elem[sy][sx] == 0:
                    continue  

                nx = x + (sx - self.radius_x)
                ny = y + (sy - self.radius_y)
                nx, ny = self._clamp_coords(nx, ny, w, h)

                values.append(bin_data[ny][nx])

        return values

    def _clamp_coords(self, x, y, w, h):
        cx = max(0, min(x, w - 1))
        cy = max(0, min(y, h - 1))
        return cx, cy
