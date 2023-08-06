from math import ceil

from django.core.paginator import Page, Paginator


class MyPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        self.delta_first = kwargs.pop('delta_first', 0)
        super().__init__(*args, **kwargs)

    def page(self, number):
        number = self.validate_number(number)
        if number == 1:
            bottom = 0
            top = self.per_page - self.delta_first
        else:
            bottom = (number - 1) * self.per_page - self.delta_first
            top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)

    @property
    def num_pages(self):
        if self.count == 0 and not self.allow_empty_first_page:
            return 0
        count = max(self.count - self.per_page + self.delta_first, 0)
        hits = max(0, count - self.orphans)
        return 1 + ceil(hits / self.per_page)
