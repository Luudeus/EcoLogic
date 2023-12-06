class Pagination:
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        # Calcula el total de páginas
        return max(0, self.total_count - 1) // self.per_page + 1

    @property
    def has_prev(self):
        # Verifica si hay una página anterior
        return self.page > 1

    @property
    def has_next(self):
        # Verifica si hay una página siguiente
        return self.page < self.pages

    @property
    def next_num(self):
        # Devuelve el número de la página siguiente
        return self.page + 1 if self.has_next else None

    @property
    def prev_num(self):
        # Devuelve el número de la página anterior
        return self.page - 1 if self.has_prev else None

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        # Itera sobre el rango de números de página para la paginación
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num