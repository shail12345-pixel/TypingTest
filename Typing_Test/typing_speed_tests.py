"""
typing_test/tests.py
Unit tests for the core framework components.
Run with: python -m pytest tests.py -v
"""
# the engine is not inporting from the SystemOS
#the issue lies within the system itself; its not pulling the right information from the engine, doesnt exist??
import time
import pytest
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from engine import TypingEngine, TestResult
from prompts import PromptLibrary

# ── TypingEngine ─────────────────────────────────────────────────────────────

class TestTypingEngine:
    PROMPT = "the quick brown fox"

    def _finish(self, typed: str, duration: float = 30.0) -> TestResult:
        """Helper: create an engine and fake-finish it."""
        engine = TypingEngine(self.PROMPT)
        engine._start_time = time.perf_counter() - duration
        return engine.finish(typed)


    def test_perfect_accuracy(self):
        result = self._finish(self.PROMPT)
        
        assert result.accuracy == 100.0
        assert result.errors == 0

    def test_wpm_calculation(self):
        # 19 chars typed in 30s → (19/5) / (30/60) = 3.8 / 0.5 = 7.6 WPM
        result = self._finish(self.PROMPT, duration=30.0)
        assert abs(result.raw_wpm - 7.6) < 0.1

    def test_accuracy_with_errors(self):
        # Replace last 3 chars with 'XXX'
        typed = self.PROMPT[:-3] + "XXX"
        result = self._finish(typed)
        assert result.errors >= 1
        assert result.accuracy < 100.0

    def test_empty_input(self):
        result = self._finish("", duration=5.0)
        assert result.wpm == 0.0
        assert result.accuracy == 0.0

    def test_finish_before_start_raises(self):
        engine = TypingEngine(self.PROMPT)
        with pytest.raises(RuntimeError):
            engine.finish("hello")

    def test_elapsed(self):
        engine = TypingEngine(self.PROMPT)
        engine.start()
        time.sleep(0.05)
        assert engine.elapsed >= 0.05


# ── PromptLibrary ─────────────────────────────────────────────────────────────

class TestPromptLibrary:
    def test_get_returns_string(self):
        lib = PromptLibrary()
        prompt = lib.get("easy")
        assert isinstance(prompt, str) and len(prompt) > 0
    #the easy version is when the prompt generation becomes at a standard pace, with accuracy below average.
    def test_seed_reproducible(self):
        lib = PromptLibrary()
        a = lib.get("medium", seed=42)
        b = lib.get("medium", seed=42)
        assert a == b
    # the medium Prompt exepcts the user so that the words get longer and sentences more academic.
    def test_different_seeds_may_differ(self):
        lib = PromptLibrary()
        results = {lib.get("medium", seed=i) for i in range(20)}
        assert len(results) > 1  # at least some variety

    def test_add_custom_prompt(self):
        lib = PromptLibrary()
        lib.add("easy", "hello world this is a custom prompt")
        assert lib.count("easy") > 5  # was 5 built-ins

    def test_all_difficulties_present(self):
        lib = PromptLibrary()
        for diff in ("easy", "medium", "hard", "code"):
            assert lib.count(diff) > 0

    def test_load_file(self, tmp_path):

        f = tmp_path / "prompts.txt"
        f.write_text("# comment\n\nfirst custom prompt\nsecond custom prompt\n") #this needs to be a string
        lib = PromptLibrary(extra_file=str(f))
        assert lib.count("custom") == 2
        assert lib.count("remodel") == 2 #
   

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
else:
    print("num py isnt actually applying itself.")
    