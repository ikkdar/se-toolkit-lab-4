"""Unit tests for interaction filtering logic - edge cases and boundary values."""

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_negative_max_item_id_excludes_all_positive() -> None:
    """Negative max_item_id should filter out all positive item_id interactions."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 5), _make_log(3, 3, 10)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=-1)
    assert result == []


def test_filter_zero_max_item_id_excludes_positive_item_ids() -> None:
    """max_item_id=0 should exclude all positive item_id interactions."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert result == []


def test_filter_zero_max_item_id_includes_zero_item_id() -> None:
    """max_item_id=0 should include interactions with item_id=0."""
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert len(result) == 1
    assert result[0].id == 1


