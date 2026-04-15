#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════╗
║          O S I N T   O R   F I C T I O N ?           ║
║     A threat intelligence game. Try not to die.      ║
╚═══════════════════════════════════════════════════════╝

Can you tell a malicious IP from a legitimate one?
The kraken is betting you can't.
"""

import random
import sys
import time
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from rich.rule import Rule
from rich.columns import Columns
from rich.align import Align
from rich.prompt import Prompt

from kraken import get_kraken
from api import (
    check_ip,
    get_demo_verdict,
    DEMO_TARGETS,
    MALICIOUS_THRESHOLD,
    IPVerdict,
)

load_dotenv()

console = Console()

MAX_LIVES = 3
POINTS_PER_CORRECT = 10
STREAK_BONUS = 5  # bonus per correct answer when on a streak >= 3

WRONG_TAUNTS = [
    "The kraken felt that one.",
    "A tentacle twitched. Not a good sign.",
    "The abyss noted your incompetence.",
    "Something large is ascending.",
    "You can hear something vast breathing.",
    "Bubbles. Large, menacing bubbles.",
    "The deep grows impatient.",
]

RIGHT_TAUNTS = [
    "Correct. Don't get smug.",
    "Lucky guess. It won't last.",
    "The kraken is... unimpressed.",
    "Right. For now.",
    "Correct. The abyss is briefly patient.",
    "Even a stopped clock, etc.",
    "Fine. You get to keep breathing. For now.",
]

STREAK_TAUNTS = [
    "A streak? The kraken is annoyed.",
    "Show-off. The tentacles are taking notes.",
    "Impressive. Infuriatingly so.",
    "You're making this look easy. Stop that.",
]


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def draw_header():
    title = Text()
    title.append("◈  O S I N T  ", style="bold cyan")
    title.append("or", style="bold white")
    title.append("  F I C T I O N ?  ◈", style="bold cyan")
    console.print(Panel(Align.center(title), style="cyan", padding=(0, 4)))


def draw_status(score: int, lives: int, streak: int, wrong: int):
    hearts = ("❤ " * lives).strip() + ("🖤 " * (MAX_LIVES - lives)).strip()
    status = Table.grid(padding=(0, 3))
    status.add_column(justify="left")
    status.add_column(justify="center")
    status.add_column(justify="right")
    status.add_row(
        f"[cyan]SCORE:[/cyan] [bold white]{score}[/bold white]",
        f"[magenta]{hearts}[/magenta]",
        f"[cyan]STREAK:[/cyan] [bold yellow]{streak}[/bold yellow]",
    )
    console.print(status)
    console.print()


def draw_kraken(wrong: int):
    art, caption = get_kraken(wrong)
    console.print(art)
    console.print(Align.center(caption))
    console.print()


def draw_target_card(ip: str, question_num: int, total: int, live_api: bool):
    api_badge = "[green]◉ LIVE API[/green]" if live_api else "[yellow]◎ DEMO MODE[/yellow]"
    console.print(
        Panel(
            f"\n[bold white]  {ip}  [/bold white]\n",
            title=f"[cyan]TARGET #{question_num}/{total}[/cyan]",
            subtitle=api_badge,
            style="magenta",
            padding=(0, 4),
        )
    )


def draw_reveal(verdict: IPVerdict, player_correct: bool, flavor: str):
    if verdict.is_malicious:
        verdict_text = f"[red bold]✗ MALICIOUS[/red bold]  (Confidence: {verdict.confidence_score}%  |  Reports: {verdict.total_reports})"
        verdict_style = "red"
    else:
        verdict_text = f"[green bold]✓ BENIGN[/green bold]  (Confidence: {verdict.confidence_score}%  |  Reports: {verdict.total_reports})"
        verdict_style = "green"

    result_icon = "[green]✔ CORRECT[/green]" if player_correct else "[red]✘ WRONG[/red]"

    details = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    details.add_column(style="bright_black", justify="right")
    details.add_column()
    details.add_row("VERDICT", verdict_text)
    details.add_row("COUNTRY", f"[white]{verdict.country}[/white]")
    details.add_row("ISP", f"[white]{verdict.isp}[/white]")
    if verdict.domain:
        details.add_row("DOMAIN", f"[white]{verdict.domain}[/white]")

    console.print(
        Panel(
            details,
            title=f"{result_icon}  [italic]{flavor}[/italic]",
            style=verdict_style,
            padding=(0, 2),
        )
    )


def draw_game_over(score: int, questions_asked: int):
    draw_kraken(3)
    console.print()
    console.print(
        Panel(
            Align.center(
                f"\n[red bold]CONSUMED BY THE ABYSS[/red bold]\n\n"
                f"[white]Final Score: [bold cyan]{score}[/bold cyan][/white]\n"
                f"[white]Survived: [bold cyan]{questions_asked}[/bold cyan] rounds[/white]\n\n"
                f"[bright_black italic]The kraken found you... adequate.[/bright_black italic]\n"
            ),
            style="red",
            padding=(1, 6),
        )
    )


def draw_victory(score: int, questions_asked: int):
    console.print()
    console.print(
        Panel(
            Align.center(
                f"\n[cyan bold]◈  YOU SURVIVED THE ABYSS  ◈[/cyan bold]\n\n"
                f"[white]Final Score: [bold magenta]{score}[/bold magenta][/white]\n"
                f"[white]Correct: [bold cyan]{questions_asked}[/bold cyan] targets analyzed[/white]\n\n"
                f"[bright_black italic]The kraken is disappointed and will try again next time.[/bright_black italic]\n"
            ),
            style="cyan",
            padding=(1, 6),
        )
    )


def prompt_guess() -> str:
    """Prompt for M (malicious) or B (benign). Returns 'M' or 'B'."""
    console.print("[cyan]Your verdict:[/cyan]  [[bold magenta]M[/bold magenta]]alicious  or  [[bold cyan]B[/bold cyan]]enign?  [bright_black](q to quit)[/bright_black]")
    while True:
        raw = Prompt.ask("  [magenta]>[/magenta]", console=console).strip().upper()
        if raw in ("M", "B", "Q"):
            return raw
        console.print("[red]  Just M or B. The kraken doesn't offer other options.[/red]")


def run_intro():
    clear()
    draw_header()
    console.print()
    console.print(
        Panel(
            "[white]You are shown a series of IP addresses.[/white]\n"
            "[white]For each one: is it [red bold]MALICIOUS[/red bold] or [green bold]BENIGN[/green bold]?[/white]\n\n"
            "[bright_black]Powered by [cyan]AbuseIPDB[/cyan] threat intelligence.\n"
            f"Confidence threshold: [cyan]{MALICIOUS_THRESHOLD}%[/cyan] = malicious.\n"
            "Get [red]3 wrong[/red] and the kraken eats you.[/bright_black]",
            title="[cyan]HOW TO PLAY[/cyan]",
            style="cyan",
            padding=(1, 4),
        )
    )
    console.print()
    Prompt.ask("[magenta]  Press Enter to descend into the abyss[/magenta]", default="", console=console)


def build_round_targets(use_api: bool) -> list[tuple]:
    """
    Build a shuffled list of (ip, pre_verdict_or_none, flavor_text) tuples.
    In demo mode, returns demo entries. In API mode, returns IPs to check live.
    """
    targets = list(DEMO_TARGETS)
    random.shuffle(targets)
    return targets


def play():
    run_intro()

    api_key = os.environ.get("ABUSEIPDB_API_KEY", "")
    use_api = bool(api_key)

    if not use_api:
        console.print(
            Panel(
                "[yellow]No ABUSEIPDB_API_KEY found in environment.\n"
                "Running in [bold]demo mode[/bold] with curated targets.\n"
                "Get a free key at [cyan]https://www.abuseipdb.com/register[/cyan][/yellow]",
                style="yellow",
                padding=(0, 2),
            )
        )
        console.print()
        time.sleep(2)

    targets = build_round_targets(use_api)

    score = 0
    lives = MAX_LIVES
    wrong_count = 0
    streak = 0
    question_num = 0
    total_questions = len(targets)

    for entry in targets:
        question_num += 1
        ip = entry[0]
        flavor_text = entry[6]  # always from demo list for flavor

        clear()
        draw_header()
        draw_status(score, lives, streak, wrong_count)
        draw_kraken(wrong_count)
        draw_target_card(ip, question_num, total_questions, use_api)

        # Get verdict
        if use_api:
            verdict = check_ip(ip)
            if verdict is None:
                console.print("[yellow]API call failed, falling back to demo data.[/yellow]")
                verdict = get_demo_verdict(entry)
        else:
            verdict = get_demo_verdict(entry)

        guess = prompt_guess()

        if guess == "Q":
            console.print("\n[bright_black]Retreating from the abyss. Cowardly, but valid.[/bright_black]")
            sys.exit(0)

        player_says_malicious = guess == "M"
        player_correct = player_says_malicious == verdict.is_malicious

        clear()
        draw_header()
        draw_status(score, lives, streak, wrong_count)

        if player_correct:
            streak += 1
            if streak >= 3:
                bonus = STREAK_BONUS
                score += POINTS_PER_CORRECT + bonus
                taunt = random.choice(STREAK_TAUNTS) + f"  [yellow](+{POINTS_PER_CORRECT + bonus} streak bonus)[/yellow]"
            else:
                score += POINTS_PER_CORRECT
                taunt = random.choice(RIGHT_TAUNTS) + f"  [cyan](+{POINTS_PER_CORRECT})[/cyan]"
        else:
            lives -= 1
            wrong_count += 1
            streak = 0
            taunt = random.choice(WRONG_TAUNTS)

        draw_kraken(wrong_count)
        draw_reveal(verdict, player_correct, taunt)

        # Show the flavor text
        console.print(f"\n  [bright_black italic]{flavor_text}[/bright_black italic]\n")

        if lives <= 0:
            time.sleep(1.5)
            clear()
            draw_game_over(score, question_num)
            console.print()
            if Prompt.ask("[magenta]Play again?[/magenta]  [y/N]", default="n", console=console).lower() == "y":
                play()
            return

        if question_num < total_questions:
            Prompt.ask("[bright_black]  Press Enter for the next target[/bright_black]", default="", console=console)

    # Survived all targets
    clear()
    draw_header()
    draw_victory(score, question_num)
    console.print()
    if Prompt.ask("[magenta]Play again?[/magenta]  [y/N]", default="n", console=console).lower() == "y":
        play()


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        console.print("\n[bright_black]The abyss will remember your retreat.[/bright_black]")
        sys.exit(0)
