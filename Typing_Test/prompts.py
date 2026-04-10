import random
from pathlib import Path


class PromptLibrary:
    _BUILTINS = {
        "easy": [
            "the quick brown fox jumps over the lazy dog",
            "a simple sentence to type quickly",
            "cats and dogs play in the sun",
            "she sells seashells by the seashore",
            "the sky is blue and the grass is green",
        ],
        "medium": [
            "programming requires patience and attention to detail",
            "the scientific method involves observation and hypothesis testing",
            "communication is the foundation of all human relationships",
            "technology continues to reshape the modern workplace significantly",
            "understanding algorithms is essential for software development",
        ],
        "hard": [
            "asynchronous programming paradigms utilize callbacks, promises, and async-await syntax",
            "the mitochondria produce adenosine triphosphate through oxidative phosphorylation",
            "bureaucratic inefficiencies perpetuate systemic organizational dysfunction unnecessarily",
            "cryptographic hash functions ensure data integrity through deterministic transformation",
            "philosophical epistemology questions the nature and scope of human knowledge",
        ],
        "code": [
            "def factorial(n): return 1 if n <= 1 else n * factorial(n - 1)",
            "for i in range(10): print(i) if i % 2 == 0 else continue",
            "const arr = [1, 2, 3].map(x => x * 2).filter(x => x > 2);",
            "SELECT * FROM users WHERE age > 18 ORDER BY name ASC;",
            "git commit -m 'fix: resolve import error in prompts module'",
        ],
    }

    def __init__(self, extra_file: str = None):
        self._prompts = {k: list(v) for k, v in self._BUILTINS.items()}
        if extra_file:
            self.load_file(extra_file)

    def get(self, difficulty: str, seed: int = None) -> str:
        rng = random.Random(seed)
        return rng.choice(self._prompts[difficulty])

    def add(self, difficulty: str, prompt: str):
        self._prompts.setdefault(difficulty, []).append(prompt)

    def count(self, difficulty: str) -> int:
        return len(self._prompts.get(difficulty, []))

    def load_file(self, path: str):
        lines = Path(path).read_text().splitlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                self._prompts.setdefault("custom", []).append(line)