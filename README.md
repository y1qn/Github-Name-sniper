# epsteins github sniper

tool i made to find available github usernames of a specific length. been using it myself for a while, finally cleaned it up enough to post

---

## what it does

generates random usernames at whatever length u want and checks if theyre actually available on github. the main thing that makes it different from other checkers is it does a double check — first hits the github api, then scrapes the actual profile page to make sure the name isnt just a banned/suspended account showing as 404. so what it tells u is available, is actually available.

also keeps a log of everything it already checked so if u close it and open it again it wont waste time on the same names twice

## how to run

you need python 3.8+, everything else installs itself when u launch it

```
py epsteins_github_sniper.py
```

We removed .bat file because it wasn't working properly.

## options

when u start it up itll ask u a few things:

- **github token** — optional but makes it way faster (5000 req/min instead of 60). u can grab one for free at github.com/settings/tokens, doesnt need any permissions
- **length** — how many chars the username should be
- **how many to find** — stops automatically once it hits that number
- **type** — letters only, numbers, mixed, or with hyphens


## Why is this file obfuscated??
I dont want anyone stealing my work :) but its a safe file trust me.
If it wasn't my acc would had gotten banbozzeld some time ago


## notes

- without a token its limited to 60 req/min by github so dont expect it to be instant
- the log file saves to ur Downloads folder as `epsteins_log.json`
- ctrl+c saves everything and exits cleanly

---

made by [github.com/y1nq](https://github.com/y1nq) — discord: xndv
