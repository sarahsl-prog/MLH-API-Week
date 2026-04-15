"""
Kraken ASCII art - 4 stages of impending doom.
Stage 0: Calm. Stage 1-2: Rising. Stage 3: You're eaten.
"""

# Color tags use Rich markup
STAGES = [
    # Stage 0: Just vibes, calm abyss
    """\
[cyan]                   *    *    *   *
              *    ~   *   ~    *
         *   ~~~  *  ~~~~~  *  ~~~  *
       ~  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ~
     [/cyan][bright_black]≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈[/bright_black]
   [bright_black]≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋[/bright_black]""",

    # Stage 1: Something stirs below...
    """\
[cyan]                   *    *    *   *
              *    ~   *   ~    *
         *   ~~~  *  ~~~~~  *  ~~~  *[/cyan]
[magenta]       )  [/magenta][cyan]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[/cyan][magenta]  ([/magenta]
[magenta]      ))  [/magenta][bright_black]≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈[/bright_black][magenta]  (([/magenta]
[magenta]     ))) [/magenta][bright_black]≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋[/bright_black][magenta] ((([/magenta]""",

    # Stage 2: Eyes. There are eyes.
    """\
[cyan]              *    ~   *   ~    *[/cyan]
[magenta]         /\\ [/magenta][cyan]~  *  ~~~~~  *  ~[/cyan][magenta] /\\[/magenta]
[magenta]        /[/magenta][yellow]()()[/yellow][magenta]\\~~~~~~~~~~~~~~~~~~/[/magenta][yellow]()()[/yellow][magenta]\\[/magenta]
[magenta]   ~~ -<( [/magenta][red]◉◉[/red][magenta] )====≈≈≈≈≈≈≈====( [/magenta][red]◉◉[/red][magenta] )>- ~~[/magenta]
[magenta]        \\__/[/magenta][bright_black]≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈[/bright_black][magenta]\\__/[/magenta]
[bright_black]   ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋[/bright_black]""",

    # Stage 3: You are eaten. This is fine.
    """\
[magenta]         ______[/magenta][red]( CRUNCH )[/red][magenta]______[/magenta]
[magenta]        /  [/magenta][red]◉[/red][magenta]  \\_________/  [/magenta][red]◉[/red][magenta]  \\[/magenta]
[magenta]       |    \\                /    |[/magenta]
[magenta]       |     \\  [/magenta][yellow]YOU ARE[/yellow][magenta]  /     |[/magenta]
[magenta]       |  /\\ /\\[/magenta][yellow]  LUNCH  [/yellow][magenta]/\\ /\\  |[/magenta]
[magenta]        \\ \\/  \\____________/  \\/ /[/magenta]
[magenta]    ~~~~-<>=====( [/magenta][red]◉◉◉◉◉[/red][magenta] )=====>-<~~~~[/magenta]
[magenta]   /)))  \\     /~~~~~~~~~~~~\\     /  ((([/magenta]
[magenta]  /  ))) \\___/ ~~~~~~~~~~~~~ \\___/ (((  [/magenta]
[bright_black]≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋[/bright_black]""",
]

STAGE_CAPTIONS = [
    "[cyan]The abyss is quiet. Suspiciously quiet.[/cyan]",
    "[magenta]Something large is noticing you.[/magenta]",
    "[magenta]It has [red]eyes[/red][magenta]. Multiple.[/magenta]",
    "[red bold]THE KRAKEN FEEDS.[/red bold]",
]

def get_kraken(wrong_count: int) -> tuple[str, str]:
    """Returns (ascii_art, caption) for the given wrong answer count."""
    stage = min(wrong_count, 3)
    return STAGES[stage], STAGE_CAPTIONS[stage]
