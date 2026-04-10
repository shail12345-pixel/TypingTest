import time
import os
from engine import TypingEngine
from prompts import PromptLibrary

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    lib = PromptLibrary()

    print("=== Typing Speed Test ===\n")
    print("Choose a difficulty:")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard")
    print("  4. Code")

    choices = {"1": "easy", "2": "medium", "3": "hard", "4": "code"}
    while True:
        pick = input("\nEnter 1-4: ").strip()
        if pick in choices:
            difficulty = choices[pick]
            break
        print("Invalid choice, try again.")

    prompt = lib.get(difficulty, seed=int(time.time()))

    clear()
    print("=== Typing Speed Test ===\n")
    print("Type the following text and press Enter when done:\n")
    print(f"  {prompt}\n")
    print("Press Enter to start...")
    input()

    engine = TypingEngine(prompt)
    engine.start()

    typed = input(">>> ")
    result = engine.finish(typed)

    clear()
    print("=== Results ===\n")
    print(f"  WPM:      {result.wpm:.1f}")
    print(f"  Raw WPM:  {result.raw_wpm:.1f}")
    print(f"  Accuracy: {result.accuracy:.1f}%")
    print(f"  Errors:   {result.errors}")
    print(f"  Time:     {result.duration:.1f}s")
    print()

if __name__ == "__main__":
    main()
