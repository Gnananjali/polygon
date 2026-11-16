from abc import ABC, abstractmethod


class StorageBackend(ABC):
    """What the migration code needs from any storage provider."""

    @abstractmethod
    def upload(self, key: str, data: bytes) -> None:
        """Save data under key, replacing anything already there."""

    @abstractmethod
    def delete_prefix(self, prefix: str) -> int:
        """Delete every file whose name starts with prefix. Returns how many."""


def problem_prefix(problem_id) -> str:
    return f"test_cases/{problem_id}/"


def test_input_key(problem_id, test_number: int) -> str:
    return f"test_cases/{problem_id}/{test_number:02d}"


def test_output_key(problem_id, test_number: int) -> str:
    return f"test_cases/{problem_id}/{test_number:02d}.a"