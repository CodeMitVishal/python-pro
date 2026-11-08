"""Tests for tasky.store. Run from tasky_project after `pip install -e ".[dev]"`:
    pytest
(Module 16 explains pytest and the tmp_path fixture.)"""
import pytest

from tasky.store import TaskStore


def test_add_assigns_increasing_ids(tmp_path):
    store = TaskStore(tmp_path / "tasks.json")
    assert store.add("a").id == 1
    assert store.add("b").id == 2


def test_complete_marks_task_done(tmp_path):
    store = TaskStore(tmp_path / "tasks.json")
    store.add("write tests")
    store.complete(1)
    assert store.load()[0].done is True


def test_complete_unknown_id_raises(tmp_path):
    with pytest.raises(KeyError):
        TaskStore(tmp_path / "tasks.json").complete(99)
