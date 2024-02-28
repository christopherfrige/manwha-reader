class GetLimitOffsetUseCase:
    @staticmethod
    def execute(page: int, per_page: int) -> tuple[int, int]:
        limit = per_page * page
        offset = (page - 1) * per_page
        return limit, offset
