class GetLimitOffsetUseCase:
    @staticmethod
    def execute(page: int, per_page: int) -> tuple[int, int]:
        if page <= 0 or per_page <= 0:
            raise ValueError

        limit = per_page * page
        offset = (page - 1) * per_page
        return limit, offset