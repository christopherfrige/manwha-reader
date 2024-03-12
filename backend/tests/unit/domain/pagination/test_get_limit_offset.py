import pytest
from src.domain.use_cases.pagination.get_limit_offset import (
    GetLimitOffsetUseCase,
)


class TestGetLimitOffsetUseCase:
    use_case = GetLimitOffsetUseCase

    @pytest.mark.parametrize(
        "page, per_page, expected_limit, expected_offset",
        [(1, 5, 5, 0), (2, 5, 10, 5), (1000, 100, 100000, 99900)],
    )
    def test_success_for_normal_parameters(self, page, per_page, expected_limit, expected_offset):
        page = page
        per_page = per_page
        limit, offset = self.use_case.execute(page, per_page)

        assert limit == expected_limit
        assert offset == expected_offset

    @pytest.mark.parametrize("page, per_page", [(-1, 5), (2, -5), (-1, -10)])
    def test_raise_value_error_for_negative_parameters(self, page, per_page):
        page = page
        per_page = per_page
        with pytest.raises(ValueError):
            self.use_case.execute(page, per_page)
