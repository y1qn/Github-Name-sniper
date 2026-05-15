import subprocess
import sys
import os

# ── auto install dependencies ────────────────────────────────
REQUIRED = ["aiohttp"]

def install_deps():
    print("\n  [*] checking dependencies...")
    for pkg in REQUIRED:
        try:
            __import__(pkg)
        except ImportError:
            print(f"  [*] installing {pkg}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    print("  [*] yeah we're good, booting up...\n")

install_deps()

# ── imports ──────────────────────────────────────────────────
import asyncio
import aiohttp
import random
import string
import time
import json
import signal
from datetime import datetime

# ============================================================
#
#   ███████╗██████╗ ███████╗████████╗███████╗██╗███╗   ██╗███████╗
#   ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║████╗  ██║██╔════╝
#   █████╗  ██████╔╝███████╗   ██║   █████╗  ██║██╔██╗ ██║███████╗
#   ██╔══╝  ██╔═══╝ ╚════██║   ██║   ██╔══╝  ██║██║╚██╗██║╚════██║
#   ███████╗██║     ███████║   ██║   ███████╗██║██║ ╚████║███████║
#   ╚══════╝╚═╝     ╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
#
#            ⚔  G I T H U B   S N I P E R  ⚔
#                  discord: xndv
#
# ============================================================

R  = "\033[91m"
G  = "\033[92m"
Y  = "\033[93m"
C  = "\033[96m"
GR = "\033[90m"
W  = "\033[97m"
M  = "\033[95m"
BO = "\033[1m"
DM = "\033[2m"
RS = "\033[0m"

# GitHub API: 60 req/min unauthenticated → ~1 req/s safe
# With a token: 5000/min → can go much faster
CONCURRENT  = 5
DELAY       = 1.1   # seconds between requests per coroutine

DOWNLOADS   = os.path.join(os.path.expanduser("~"), "Downloads")
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
LOG_FILE    = os.path.join(DOWNLOADS, "epsteins_log.json")

STOP = False
LOG  = None

LARPER_TAUNTS = [
    "bro that name was cooked anyway 💀",
    "another one bites the dust frfr",
    "nah this one was mid tbh",
    "gone. reduced to atoms.",
    "this username never stood a chance",
    "rip bozo fr fr",
    "another casualty of the snipe",
    "that one was cursed from birth",
    "deleted just like my social life",
]

LARPER_FINDS = [
    "YO WE COOKED 🔥🔥🔥",
    "BRO ACTUALLY ATE 💀",
    "NO WAY THIS IS REAL",
    "SLAY ACTUALLY SLAY",
    "we so back omg",
    "GRAB IT BEFORE SOMEONE ELSE DOES",
    "LETS GOOOOO FINALLY",
    "the prophecy was real",
    "i knew we'd find something good",
]

# ─── SIGNAL HANDLER ─────────────────────────────────────────

def handle_exit(sig=None, frame=None):
    global STOP
    STOP = True
    if LOG is not None:
        save_log(LOG)
        print(f"\n  {Y}yo we out — dumped {len(LOG['checked'])} names to ur Downloads, don't lose it{RS}\n")
    sys.exit(0)

signal.signal(signal.SIGINT,  handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# ─── LOG ────────────────────────────────────────────────────

def load_log():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"checked": {}, "available": [], "sessions": 0}

def save_log(log):
    try:
        os.makedirs(DOWNLOADS, exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2)
    except Exception:
        pass

def log_result(log, username, result):
    if STOP:
        return
    log["checked"][username] = {
        "result": result,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if result == "available" and username not in log["available"]:
        log["available"].append(username)
    if len(log["checked"]) % 5 == 0:
        save_log(log)

# ─── UI ─────────────────────────────────────────────────────

DG = "\033[32m"   # dark green (pixel on)
BK = "\033[90m"   # dim (pixel off)
_O = f"{DG}▪{BK}"  # pixel on
__ = f"{BK} {BK}"  # pixel off

FACE = (
    f"{BK}  "
    + f"{__}{__}{__}{__}{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}{__}{__}{__}{__}\n  "
    + f"{__}{__}{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}{__}\n  "
    + f"{__}{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}\n  "
    + f"{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}\n  "
    + f"{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{_O}{_O}{_O}{__}{__}{_O}{_O}{_O}{__}{__}{_O}{_O}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{_O}{_O}{__}{__}{__}{_O}{_O}{_O}{__}{__}{__}{_O}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{_O}{__}{__}{__}{__}{_O}{_O}{_O}{__}{__}{__}{__}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{__}{__}{__}{__}{__}{__}{__}{__}{__}{__}{__}{__}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}{_O}{_O}{_O}\n  "
    + f"{_O}{_O}{_O}{_O}{__}{__}{__}{__}{__}{__}{__}{__}{__}{__}{_O}{_O}{_O}{_O}\n  "
    + f"{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}\n  "
    + f"{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}\n  "
    + f"{__}{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}{__}\n  "
    + f"{__}{__}{__}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{_O}{__}{__}{__}{__}"
    + RS
)

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(FACE)
    print(f"  {DG}{BO}╔══════════════════════════════════════════════════╗{RS}")
    print(f"  {DG}{BO}║   ⚔   E P S T E I N S   G I T H U B   S N I P E R   ⚔   ║{RS}")
    print(f"  {DG}{BO}║        yeah we sniping github usernames rn           ║{RS}")
    print(f"  {DG}{BO}║   discord: {C}xndv{DG}   made by: {C}github.com/y1nq{DG}          ║{RS}")
    print(f"  {DG}{BO}╚══════════════════════════════════════════════════╝{RS}\n")

def credits(log):
    total_checked = len(log["checked"])
    total_avail   = len(log["available"])
    sessions      = log["sessions"]

    print(f"  {GR}┌────────────────────────────────────────────────┐{RS}")
    print(f"  {GR}│  {W}tool     {GR}»  {W}Epsteins Github Sniper            {GR}│{RS}")
    print(f"  {GR}│  {W}made by  {GR}»  {C}discord: xndv                     {GR}│{RS}")
    print(f"  {GR}│  {W}version  {GR}»  {W}3.0 — actually accurate now       {GR}│{RS}")
    print(f"  {GR}│  {W}how      {GR}»  {G}API + HTML double check            {GR}│{RS}")
    print(f"  {GR}│  {W}log      {GR}»  {Y}ur Downloads folder               {GR}│{RS}")
    print(f"  {GR}├────────────────────────────────────────────────┤{RS}")
    print(f"  {GR}│  {W}times u ran this  »  {W}{sessions:<25}{GR}│{RS}")
    print(f"  {GR}│  {W}names checked     »  {W}{total_checked:<25}{GR}│  {GR}won't redo these{RS}")
    print(f"  {GR}│  {W}hits so far       »  {G}{total_avail:<25}{GR}│{RS}")
    print(f"  {GR}└────────────────────────────────────────────────┘{RS}")

    if total_avail > 0:
        print(f"\n  {GR}names u already sniped:{RS}")
        for name in log["available"][-5:]:
            print(f"    {G}✓  {W}{name:<20}{GR}→  {C}github.com/{name}{RS}")
        if total_avail > 5:
            print(f"    {GR}... +{total_avail - 5} more chillin in the log file{RS}")
    print()

def menu():
    print(f"  {GR}┌────────────────────────────────────────────────┐{RS}")
    print(f"  {GR}│  {W}aight set it up and we'll start sniping          {GR}│{RS}")
    print(f"  {GR}└────────────────────────────────────────────────┘{RS}\n")

    print(f"  {W}got a github token?  {GR}paste it for way faster speeds (5000/min), or just hit enter to skip{RS}")
    token = input(f"  {C}» {RS}").strip()

    print(f"\n  {W}how long should the username be?  {GR}anywhere from 1 to 39{RS}")
    length = input(f"  {C}» {RS}").strip()
    try:
        length = int(length)
        if not 1 <= length <= 39:
            raise ValueError
    except ValueError:
        print(f"\n  {R}bro that's not valid, pick something between 1 and 39{RS}\n")
        input("  press enter to bail...")
        sys.exit(1)

    print(f"\n  {W}how many available names u tryna find?{RS}")
    goal = input(f"  {C}» {RS}").strip()
    try:
        goal = int(goal)
        if goal < 1:
            raise ValueError
    except ValueError:
        print(f"\n  {R}yeah that's not a real number bro{RS}\n")
        input("  press enter to bail...")
        sys.exit(1)

    print(f"""
  {W}what kind of username?{RS}
  {GR}[1]{RS}  just letters        {DM}e.g. xvnz{RS}
  {GR}[2]{RS}  just numbers        {DM}e.g. 4829{RS}
  {GR}[3]{RS}  letters + numbers   {DM}e.g. x4n2{RS}
  {GR}[4]{RS}  letters with hyphen {DM}e.g. xv-nz{RS}
""")
    mode = input(f"  {C}» {RS}").strip()
    if mode not in ["1","2","3","4"]:
        mode = "1"

    return token, length, goal, mode

# ─── GENERATOR ──────────────────────────────────────────────

def generate_name(length, mode):
    alpha = string.ascii_lowercase
    nums  = string.digits
    mix   = alpha + nums

    if mode == "1":
        return ''.join(random.choices(alpha, k=length))
    elif mode == "2":
        return ''.join(random.choices(nums, k=length))
    elif mode == "3":
        return ''.join(random.choices(mix, k=length))
    elif mode == "4":
        if length < 3:
            return ''.join(random.choices(alpha, k=length))
        base = list(random.choices(alpha, k=length))
        base[random.randint(1, length - 2)] = '-'
        return ''.join(base)
    return ''.join(random.choices(alpha, k=length))

# ─── CHECKER ────────────────────────────────────────────────
#
#  GitHub REST API — GET /users/{username}
#  200  → user exists                  → taken
#  404  → user not found               → available (maybe)
#
#  BUT: deleted/suspended accounts also return 404.
#  Second check: GET github.com/{username} HTML page
#    - real 404 page  → truly available
#    - "suspended"    → suspended, skip
#    - profile page   → taken (renamed account or org)
#
# ────────────────────────────────────────────────────────────

async def check_username(session, username, semaphore, token=None):
    api_url  = f"https://api.github.com/users/{username}"
    html_url = f"https://github.com/{username}"

    api_headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "epsteins-sniper",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        api_headers["Authorization"] = f"Bearer {token}"

    html_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    async with semaphore:
        await asyncio.sleep(DELAY + random.uniform(0, 0.5))
        try:
            # ── step 1: API check ────────────────────────────
            async with session.get(
                api_url,
                headers=api_headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:

                remaining = int(resp.headers.get("X-RateLimit-Remaining", 999))
                if remaining < 3:
                    # close to rate limit — wait for reset
                    reset_at = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
                    wait = max(reset_at - int(time.time()), 5)
                    return username, f"ratelimit:{wait}"

                if resp.status == 200:
                    return username, "taken"
                elif resp.status in (403, 429):
                    return username, "ratelimit:30"
                elif resp.status != 404:
                    return username, "error"

            # ── step 2: HTML scrape to confirm availability ──
            async with session.get(
                html_url,
                headers=html_headers,
                timeout=aiohttp.ClientTimeout(total=10),
                allow_redirects=True
            ) as resp:

                if resp.status == 404:
                    # truly available — confirmed on both API and HTML
                    return username, "available"

                if resp.status == 200:
                    body = (await resp.text(errors="ignore")).lower()
                    if "this account has been suspended" in body or "suspended" in body[:3000]:
                        return username, "suspended"
                    # profile loaded = taken (renamed, org, etc.)
                    return username, "taken"

                return username, "error"

        except asyncio.TimeoutError:
            return username, "timeout"
        except Exception:
            return username, "error"

# ─── HUNT ───────────────────────────────────────────────────

async def hunt(length, goal, mode, log, token):
    global STOP
    mode_names = {"1":"letters","2":"numbers","3":"mixed","4":"letters+hyphen"}
    found     = []
    total     = 0
    taken     = 0
    suspended = 0
    errors    = 0
    start     = time.time()

    already_checked = set(log["checked"].keys())
    skipped = sum(1 for k in already_checked if len(k) == length)

    speed_mode = "5000 req/min (token)" if token else "60 req/min (no token)"

    print(f"\n{GR}  ══════════════════════════════════════════════════{RS}")
    print(f"  {W}aight let's run it{RS}")
    print(f"  {GR}length={W}{length}{RS}  {GR}goal={W}{goal}{RS}  {GR}type={W}{mode_names.get(mode,'?')}{RS}")
    print(f"  {GR}speed    »  {G}{speed_mode}{RS}")
    print(f"  {GR}checking »  {G}API first then HTML to make sure it's actually free{RS}")
    if skipped > 0:
        print(f"  {GR}skipping {Y}{skipped}{GR} names we already tried last time{RS}")
    print(f"  {GR}hit ctrl+c whenever u want to stop, the log saves itself{RS}")
    print(f"{GR}  ══════════════════════════════════════════════════{RS}\n")

    semaphore = asyncio.Semaphore(CONCURRENT)
    connector = aiohttp.TCPConnector(limit=CONCURRENT * 2)
    checked_this_session = set()

    async with aiohttp.ClientSession(connector=connector) as session:
        while len(found) < goal and not STOP:
            batch = []
            attempts = 0
            while len(batch) < CONCURRENT and attempts < 50000:
                name = generate_name(length, mode)
                if name not in already_checked and name not in checked_this_session:
                    checked_this_session.add(name)
                    batch.append(name)
                attempts += 1

            if not batch:
                print(f"\n  {Y}ran out of combos for this length and type, try changing it up{RS}")
                break

            tasks = [check_username(session, name, semaphore, token) for name in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for item in results:
                if STOP or len(found) >= goal:
                    break
                if isinstance(item, Exception):
                    errors += 1
                    continue

                username, result = item
                total += 1
                elapsed = time.time() - start
                rate = total / elapsed if elapsed > 0 else 0

                if result.startswith("ratelimit"):
                    wait = int(result.split(":")[1]) if ":" in result else 30
                    print(f"  {Y}  github's being annoying, told us to chill for {wait}s... waiting{RS}")
                    await asyncio.sleep(wait)
                    continue

                log_result(log, username, result)

                if result == "available":
                    found.append(username)
                    taunt = random.choice(LARPER_FINDS)
                    print(f"  {G}{BO}  [+] {username:<{length+2}}  AVAILABLE ✓{RS}  {GR}({len(found)}/{goal}) [{rate:.2f}/s]{RS}")
                    print(f"       {M}{taunt}{RS}")
                elif result == "suspended":
                    suspended += 1
                    print(f"  {Y}  [~] {username:<{length+2}}  banned acc, skipping that one{RS}  {GR}[{total} checked]{RS}")
                elif result == "taken":
                    taken += 1
                    taunt = random.choice(LARPER_TAUNTS)
                    print(f"  {R}  [-] {username:<{length+2}}  taken  {GR}{taunt}{RS}  {GR}[{total} · {rate:.2f}/s]{RS}")
                elif result == "timeout":
                    errors += 1
                    print(f"  {GR}  [?] {username:<{length+2}}  took too long, skipping{RS}")
                else:
                    errors += 1
                    print(f"  {GR}  [?] {username:<{length+2}}  something went wrong, moving on{RS}")

    save_log(log)
    print(f"\n  {GR}saved everything to {Y}{LOG_FILE}{RS}")
    return found, total, taken, suspended, errors, start

# ─── RESULTS ────────────────────────────────────────────────

def show_results(found, total, taken, suspended, errors, start):
    elapsed = time.time() - start
    rate = total / elapsed if elapsed > 0 else 0

    print(f"\n{GR}  ══════════════════════════════════════════════════{RS}")
    print(f"  {W}{BO}alright here's what happened{RS}")
    print(f"{GR}  ══════════════════════════════════════════════════{RS}")
    print(f"  {GR}checked    »  {W}{total}{RS}")
    print(f"  {GR}available  »  {G}{len(found)}{RS}")
    print(f"  {GR}taken      »  {R}{taken}{RS}")
    print(f"  {GR}suspended  »  {Y}{suspended}{RS}  {GR}← banned accs we skipped{RS}")
    print(f"  {GR}errors     »  {GR}{errors}{RS}")
    print(f"  {GR}time       »  {W}{elapsed:.1f}s{RS}")
    print(f"  {GR}speed      »  {G}{rate:.2f} checks/s{RS}")
    print(f"{GR}  ══════════════════════════════════════════════════{RS}\n")

    if found:
        print(f"  {G}{BO}go register these before someone else does:{RS}\n")
        for name in found:
            print(f"  {G}  ✓  {W}{name:<20}{GR}→  {C}https://github.com/{name}{RS}")
    else:
        print(f"  {Y}  nothing this run, happens — just run it again{RS}")

    print(f"\n{GR}  ══════════════════════════════════════════════════{RS}")
    print(f"  {GR}Epsteins Github Sniper — discord: {C}xndv{RS}\n")

# ─── MAIN ───────────────────────────────────────────────────

async def main():
    global LOG
    banner()
    LOG = load_log()
    LOG["sessions"] += 1
    credits(LOG)
    token, length, goal, mode = menu()
    found, total, taken, suspended, errors, start = await hunt(length, goal, mode, LOG, token or None)
    if not STOP:
        show_results(found, total, taken, suspended, errors, start)
        input(f"  {GR}press enter whenever u ready to close this{RS}")

if __name__ == "__main__":
    asyncio.run(main())
