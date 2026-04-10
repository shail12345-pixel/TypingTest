import time
from dataclasses import dataclass
import difflib
@dataclass
class TestResult:
    wpm: float
    raw_wpm: float
    accuracy: float
    errors: int
    duration: float

class TypingEngine:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self._start_time = None

    def start(self):
        self._start_time = time.perf_counter()

    @property
    def elapsed(self):
        if self._start_time is None:
            raise RuntimeError("Test has not been started.")
        return time.perf_counter() - self._start_time

    def finish(self, typed: str) -> TestResult:
        if self._start_time is None:
            raise RuntimeError("Test has not been started.")
        
        duration = time.perf_counter() - self._start_time

        if not typed:
            return TestResult(wpm=0.0, raw_wpm=0.0, accuracy=0.0, errors=0, duration=duration)

        errors = sum(1 for a, b in zip(self.prompt, typed) if a != b)
        errors += abs(len(self.prompt) - len(typed))

        accuracy = max(0.0, (1 - errors / len(self.prompt)) * 100)
        raw_wpm = (len(typed) / 5) / (duration / 60)
        wpm = raw_wpm * (accuracy / 100)

        return TestResult(wpm=wpm, raw_wpm=raw_wpm, accuracy=accuracy, errors=errors, duration=duration)
