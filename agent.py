"""
agent.py — Simulated AI Agent
A simple document summarization agent for demo purposes.
"""

import time

GRAY  = "\033[90m"
WHITE = "\033[97m"
BOLD  = "\033[1m"
RESET = "\033[0m"
DIM   = "\033[2m"


def my_agent(text):
    """
    Simulated AI agent that reads and summarizes a document.
    In production this would call an LLM like Claude or GPT-4.
    """
    print(f"  {GRAY}Agent is reading the document...{RESET}")
    time.sleep(0.6)

    words = text.strip().split()
    word_count = len(words)

    print(f"  {GRAY}Analyzing content  ({word_count} words){RESET}")
    time.sleep(0.4)

    print(f"  {GRAY}Generating summary...{RESET}")
    time.sleep(0.5)

    first_sentence = " ".join(words[:12]) + ("..." if word_count > 12 else "")
    summary = (
        f"Document processed successfully.\n"
        f"  Word count : {word_count}\n"
        f"  Preview    : {first_sentence}\n"
        f"  Status     : Summary complete"
    )
    return summary
