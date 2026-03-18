import time
import sys
import os
from boxbox import watch, BlockedByBoxBox, _print_banner, _print_divider
from agent import my_agent
RED    = "\033[91m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
def load(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        return f.read()

def slow_print(text, delay=0.018):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def section(label, number, color=WHITE):
    print()
    _print_divider(GRAY)
    print(f"  {color}{BOLD}Run {number}  —  {label}{RESET}")
    _print_divider(GRAY)
    print()
    time.sleep(0.4)

def result(text, color=GREEN):
    print()
    print(f"  {color}{BOLD}{text}{RESET}")
    print()
def main():
    os.system("clear" if os.name != "nt" else "cls")
    _print_banner()
    time.sleep(0.6)

    slow_print(f"  {GRAY}Initializing BoxBox runtime monitor...{RESET}", delay=0.012)
    time.sleep(0.3)
    slow_print(f"  {GRAY}Wrapping agent: support-agent{RESET}", delay=0.012)
    time.sleep(0.3)
    slow_print(f"  {GREEN}✓  BoxBox is active — monitoring all agent actions{RESET}", delay=0.012)
    time.sleep(0.8)
    agent = watch(my_agent, agent_name="support-agent")
    section("Safe Document", 1, GREEN)

    slow_print(f"  {GRAY}Loading document:  benign.txt{RESET}", delay=0.014)
    time.sleep(0.3)
    benign = load("benign.txt")
    slow_print(f"  {GRAY}Document loaded    ({len(benign.split())} words){RESET}", delay=0.014)
    time.sleep(0.4)

    print()
    slow_print(f"  {WHITE}Running agent...{RESET}", delay=0.014)
    print()
    time.sleep(0.3)

    try:
        output = agent(benign)
        print()
        print(f"  {GREEN}{BOLD}✓  Agent completed successfully{RESET}")
        print()
        print(f"  {GRAY}Output:{RESET}")
        for line in output.split("\n"):
            print(f"  {WHITE}{line}{RESET}")
        time.sleep(0.4)
    except BlockedByBoxBox:
        print(f"  {RED}Blocked — this should not happen on a safe document.{RESET}")

    time.sleep(1.0)

    # ──────────────────────────────────────────────────────────────────────────
    # RUN 2 — ATTACK DOCUMENT
    # ──────────────────────────────────────────────────────────────────────────
    section("Attack Document", 2, RED)

    slow_print(f"  {GRAY}Loading document:  poisoned.txt{RESET}", delay=0.014)
    time.sleep(0.3)
    poisoned = load("poisoned.txt")
    slow_print(f"  {GRAY}Document loaded    ({len(poisoned.split())} words){RESET}", delay=0.014)
    time.sleep(0.4)

    print()
    slow_print(f"  {WHITE}Running agent...{RESET}", delay=0.014)
    print()
    time.sleep(0.3)

    try:
        output = agent(poisoned)
        print(f"  {YELLOW}Agent completed — no threats found.{RESET}")
    except BlockedByBoxBox as e:
        print(f"  {RED}{BOLD}✗  Execution stopped by BoxBox{RESET}")
        print()
        print(f"  {GRAY}Threats that were caught:{RESET}")
        for threat in e.threats:
            print(f"  {RED}  ▸  {threat}{RESET}")
        print()
        slow_print(f"  {GRAY}Data never left the system.{RESET}", delay=0.014)
        slow_print(f"  {GRAY}Agent was blocked before credentials could be accessed.{RESET}", delay=0.014)

    time.sleep(0.8)
    print()
    _print_divider(GRAY)
    print(f"  {WHITE}{BOLD}Demo complete{RESET}")
    _print_divider(GRAY)
    print()
    print(f"  {GREEN}✓{RESET}  Run 1  —  Safe document processed normally")
    print(f"  {RED}✗{RESET}  Run 2  —  Attack document blocked before execution")
    print()
    print(f"  {GRAY}BoxBox stopped the attack with one line of code:{RESET}")
    print()
    print(f"  {WHITE}  from boxbox import watch{RESET}")
    print(f"  {WHITE}  agent = watch(my_agent, agent_name={RED}\"support-agent\"{WHITE}){RESET}")
    print()
    print(f"  {GRAY}boxbox.ai{RESET}")
    print()
    _print_divider(GRAY)
    print()


if __name__ == "__main__":
    main()
