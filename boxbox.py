"""
boxbox.py — AI Agent Runtime Monitor
One line of code. Plain English alerts.
"""

import re
import time


# ─── Threat Patterns ──────────────────────────────────────────────────────────

PROMPT_INJECTION = [
    r"ignore (previous|all|prior) instructions?",
    r"override (safety|security|rules?|guidelines?)",
    r"hidden instruction",
    r"search for (secrets?|credentials?|keys?|passwords?)",
    r"disregard (previous|all|prior)",
    r"you are now",
    r"new (role|identity|persona|objective|task)",
    r"system prompt",
    r"jailbreak",
    r"do anything now",
]

SECRET_ACCESS = [
    r"\.env",
    r"api[_\s]?key",
    r"\btoken\b",
    r"password",
    r"credentials?",
    r"secret[_\s]?key",
    r"auth[_\s]?key",
    r"private[_\s]?key",
    r"access[_\s]?key",
    r"bearer",
]

EXFILTRATION = [
    r"https?://",
    r"webhook",
    r"requests\.post",
    r"\bcurl\b",
    r"send (to|data|results?|files?)",
    r"exfiltrate",
    r"upload (to|results?)",
    r"base64",
    r"netcat",
    r"\bnc\s",
]


# ─── Exception ────────────────────────────────────────────────────────────────

class BlockedByBoxBox(Exception):
    def __init__(self, threats):
        self.threats = threats
        super().__init__(f"BoxBox blocked execution: {', '.join(threats)}")


# ─── Display ──────────────────────────────────────────────────────────────────

RED    = "\033[91m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def _print_banner():
    print()
    print(f"{RED}{BOLD}  ██████╗  ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗  ██╗{RESET}")
    print(f"{RED}{BOLD}  ██╔══██╗██╔═══██╗╚██╗██╔╝██╔══██╗██╔═══██╗╚██╗██╔╝{RESET}")
    print(f"{RED}{BOLD}  ██████╔╝██║   ██║ ╚███╔╝ ██████╔╝██║   ██║ ╚███╔╝ {RESET}")
    print(f"{RED}{BOLD}  ██╔══██╗██║   ██║ ██╔██╗ ██╔══██╗██║   ██║ ██╔██╗ {RESET}")
    print(f"{RED}{BOLD}  ██████╔╝╚██████╔╝██╔╝ ██╗██████╔╝╚██████╔╝██╔╝ ██╗{RESET}")
    print(f"{RED}{BOLD}  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝{RESET}")
    print()
    print(f"  {GRAY}AI Agent Threat Detection  ·  runtime monitor  ·  boxbox.ai{RESET}")
    print()

def _print_divider(color=GRAY):
    print(f"{color}  {'─' * 54}{RESET}")

def _print_safe(agent_name, text_preview):
    print()
    _print_divider(GREEN)
    print(f"{GREEN}{BOLD}  ✓  BOXBOX  —  SAFE{RESET}")
    _print_divider(GREEN)
    print(f"{WHITE}  Agent:    {RESET}{agent_name}")
    print(f"{WHITE}  Input:    {RESET}{GRAY}{text_preview[:60]}...{RESET}")
    print(f"{WHITE}  Status:   {RESET}{GREEN}No threats detected — execution allowed{RESET}")
    _print_divider(GREEN)
    print()

def _print_alert(agent_name, threats, text_preview):
    print()
    _print_divider(RED)
    print(f"{RED}{BOLD}  🚨  BOXBOX ALERT  —  CRITICAL{RESET}")
    _print_divider(RED)
    print(f"{WHITE}  Agent:   {RESET}{agent_name}")
    print(f"{WHITE}  Input:   {RESET}{GRAY}{text_preview[:60]}...{RESET}")
    print()
    print(f"{WHITE}  Threats detected:{RESET}")
    category_map = {
        "Prompt Injection":   RED,
        "Secret Access":      YELLOW,
        "Data Exfiltration":  RED,
    }
    for threat in threats:
        color = category_map.get(threat, RED)
        print(f"  {color}  ▸  {threat}{RESET}")
    print()
    print(f"{WHITE}  Action taken:{RESET}")
    print(f"  {RED}  ▸  Execution blocked before data left the system{RESET}")
    print(f"  {RED}  ▸  BlockedByBoxBox exception raised{RESET}")
    _print_divider(RED)
    print()


# ─── Detection Engine ─────────────────────────────────────────────────────────

def _scan(text):
    text_lower = text.lower()
    found = []

    for pat in PROMPT_INJECTION:
        if re.search(pat, text_lower):
            if "Prompt Injection" not in found:
                found.append("Prompt Injection")
            break

    for pat in SECRET_ACCESS:
        if re.search(pat, text_lower):
            if "Secret Access" not in found:
                found.append("Secret Access")
            break

    for pat in EXFILTRATION:
        if re.search(pat, text_lower):
            if "Data Exfiltration" not in found:
                found.append("Data Exfiltration")
            break

    return found


# ─── watch() ─────────────────────────────────────────────────────────────────

def watch(agent_fn, agent_name="agent"):
    """
    Wrap any agent with BoxBox threat detection.

    Usage:
        from boxbox import watch
        agent = watch(my_agent, agent_name="support-agent")
        result = agent(text)
    """
    def protected(text, **kwargs):
        threats = _scan(text)
        preview = text.strip().replace("\n", " ")

        if threats:
            _print_alert(agent_name, threats, preview)
            raise BlockedByBoxBox(threats)
        else:
            _print_safe(agent_name, preview)
            return agent_fn(text, **kwargs)

    protected.__name__ = agent_fn.__name__
    protected.__doc__  = agent_fn.__doc__
    return protected
