# Data Overview — NFL Improv Score

Source: cloned from `weswidjo/nfl-big-data-bowl-regional-event-data`, data files
copied into `data/raw/` (the `tracking/` subfolder preserved). Data is gitignored.

**Season:** 2021, weeks 1–8. **Tracking frame rate:** 10 fps.

> Note: this overview was generated with Python's built-in `csv` module because the
> sandbox has no internet access to install pandas. The same information (shape,
> columns, sample rows, value counts) is captured below. See `inspect_data.py`.

---

## Files in `data/raw/`

| File | Rows | Columns |
|------|-----:|--------:|
| games.csv | 122 | 7 |
| players.csv | 1,679 | 7 |
| plays.csv | 8,557 | 32 |
| pffScoutingData.csv | 188,254 | 15 |
| tracking/*.csv | 8,314,178 (across 122 files) | 16 |

---

## games.csv — 122 rows × 7 columns

**Columns:** `gameId, season, week, gameDate, gameTimeEastern, homeTeamAbbr, visitorTeamAbbr`

One row per game (122 games = the 122 tracking files). Sample rows:

1. `gameId=2021090900, season=2021, week=1, gameDate=09/09/2021, gameTimeEastern=20:20:00, homeTeamAbbr=TB, visitorTeamAbbr=DAL`
2. `gameId=2021091200, season=2021, week=1, gameDate=09/12/2021, gameTimeEastern=13:00:00, homeTeamAbbr=ATL, visitorTeamAbbr=PHI`
3. `gameId=2021091201, season=2021, week=1, gameDate=09/12/2021, gameTimeEastern=13:00:00, homeTeamAbbr=BUF, visitorTeamAbbr=PIT`

---

## players.csv — 1,679 rows × 7 columns

**Columns:** `nflId, height, weight, birthDate, collegeName, officialPosition, displayName`

One row per player. `nflId` is the key that links to tracking and pff data. Sample rows:

1. `nflId=25511, height=6-4, weight=225, birthDate=1977-08-03, collegeName=Michigan, officialPosition=QB, displayName=Tom Brady`
2. `nflId=28963, height=6-5, weight=240, birthDate=1982-03-02, collegeName=Miami, O., officialPosition=QB, displayName=Ben Roethlisberger`
3. `nflId=29550, height=6-4, weight=328, birthDate=1982-01-22, collegeName=Arkansas, officialPosition=T, displayName=Jason Peters`

---

## plays.csv — 8,557 rows × 32 columns

**Columns:** `gameId, playId, playDescription, quarter, down, yardsToGo, possessionTeam,
defensiveTeam, yardlineSide, yardlineNumber, gameClock, preSnapHomeScore,
preSnapVisitorScore, passResult, penaltyYards, prePenaltyPlayResult, playResult,
foulName1, foulNFLId1, foulName2, foulNFLId2, foulName3, foulNFLId3,
absoluteYardlineNumber, offenseFormation, personnelO, defendersInBox, personnelD,
dropBackType, pff_playAction, pff_passCoverage, pff_passCoverageType`

One row per play. `gameId + playId` is the key. Sample rows (abbreviated):

1. `2021090900 / 97` — "(13:33) (Shotgun) T.Brady pass incomplete deep right to C.Godwin." — passResult=I, dropBackType=TRADITIONAL, coverage=Cover-1 (Man)
2. `2021090900 / 137` — "(13:18) D.Prescott pass deep left to A.Cooper … 28 yards" — passResult=C, dropBackType=TRADITIONAL, coverage=Cover-3 (Zone)
3. `2021090900 / 187` — "(12:23) D.Prescott pass short middle to D.Schultz … 5 yards" — passResult=C, dropBackType=TRADITIONAL, coverage=Cover-3 (Zone)

### Value counts — `dropBackType`

| value | count |
|-------|------:|
| TRADITIONAL | 6,542 |
| SCRAMBLE | 899 |
| NA | 528 |
| DESIGNED_ROLLOUT_RIGHT | 285 |
| DESIGNED_ROLLOUT_LEFT | 149 |
| SCRAMBLE_ROLLOUT_RIGHT | 125 |
| SCRAMBLE_ROLLOUT_LEFT | 23 |
| DESIGNED_RUN | 5 |
| UNKNOWN | 1 |

**Relevant to Improv Score:** `SCRAMBLE` (899) + `SCRAMBLE_ROLLOUT_RIGHT` (125) +
`SCRAMBLE_ROLLOUT_LEFT` (23) = **1,047 plays where the QB broke the pocket and
improvised** — these are the "play falls apart" moments at the heart of the project.

### Value counts — `passResult`

| value | meaning | count |
|-------|---------|------:|
| C | Complete | 4,620 |
| I | Incomplete | 2,755 |
| S | Sack | 543 |
| R | Scramble (QB ran) | 449 |
| IN | Interception | 190 |

(Rows where `passResult` is blank are non-dropback plays; total non-blank = 8,557.)

---

## pffScoutingData.csv — 188,254 rows × 15 columns

**Columns:** `gameId, playId, nflId, pff_role, pff_positionLinedUp, pff_hit,
pff_hurry, pff_sack, pff_beatenByDefender, pff_hitAllowed, pff_hurryAllowed,
pff_sackAllowed, pff_nflIdBlockedPlayer, pff_blockType, pff_backFieldBlock`

One row per player per play (PFF scouting charting). Key = `gameId + playId + nflId`.
`pff_role` tells us each player's job on the play (e.g. `Pass`, `Pass Route`,
`Pass Block`, `Coverage`) — useful for isolating the receivers running routes.
Sample rows:

1. `2021090900 / 97 / 25511` — pff_role=Pass, positionLinedUp=QB (this is the QB)
2. `2021090900 / 97 / 35481` — pff_role=Pass Route, positionLinedUp=TE-L
3. `2021090900 / 97 / 35634` — pff_role=Pass Route, positionLinedUp=LWR

---

## tracking/ — 122 files, 8,314,178 rows total, 16 columns each

**Organization:** one CSV per game, named `tracking_<gameId>.csv`
(e.g. `tracking_2021090900.csv`). The `<gameId>` matches `games.csv`/`plays.csv`.
Example filenames: `tracking_2021090900.csv`, `tracking_2021091200.csv`,
`tracking_2021091201.csv`, …

**Columns:** `gameId, playId, nflId, frameId, time, jerseyNumber, team,
playDirection, x, y, s, a, dis, o, dir, event`

- Frames are 10 fps; `frameId` increments within a play.
- `x, y` = field position (yards); `s` = speed, `a` = acceleration, `dis` =
  distance moved since last frame; `o` = orientation, `dir` = direction of motion.
- `playDirection` (left/right) matters for normalizing coordinates.
- The football itself appears as rows with `team=football` / no `nflId`.
- `event` marks key moments on a frame (most frames have no event).

Sample rows (from `tracking_2021090900.csv`, play 97, Tom Brady nflId 25511):

1. `frameId=1, x=37.77, y=24.22, s=0.29, a=0.3, dir=84.99, event=None`
2. `frameId=2, x=37.78, y=24.22, s=0.23, a=0.11, dir=92.87, event=None`
3. `frameId=3, x=37.78, y=24.24, s=0.16, a=0.1, dir=68.55, event=None`

### Unique `event` values (27, across all tracking files)

| event | count |
|-------|------:|
| None (no event this frame) | 7,673,352 |
| ball_snap | 196,236 |
| pass_forward | 173,604 |
| autoevent_ballsnap | 86,641 |
| autoevent_passforward | 85,882 |
| play_action | 45,471 |
| run | 10,902 |
| qb_sack | 10,373 |
| pass_arrived | 8,441 |
| autoevent_passinterrupted | 4,623 |
| man_in_motion | 4,071 |
| line_set | 3,220 |
| shift | 3,059 |
| pass_tipped | 2,553 |
| first_contact | 1,840 |
| qb_strip_sack | 1,334 |
| pass_outcome_incomplete | 920 |
| pass_outcome_caught | 529 |
| fumble | 391 |
| fumble_offense_recovered | 253 |
| handoff | 230 |
| huddle_break_offense | 69 |
| tackle | 69 |
| penalty_flag | 46 |
| lateral | 23 |
| dropped_pass | 23 |
| out_of_bounds | 23 |

**Relevant to Improv Score:** `ball_snap` marks the start of the play; `pass_forward`
marks when the QB throws. The stretch *between* snap and throw — especially when it
runs long or the QB scrambles (`qb_sack`, `qb_strip_sack` for failures) — is the
window where receivers improvise to get open.

---

## Takeaways for the Improv Score

- **"Play falls apart" signal is available two ways:** `dropBackType` in plays.csv
  flags ~1,047 scramble plays directly, and the gap between `ball_snap` and
  `pass_forward` in tracking tells us how long the play was extended.
- **Receivers to measure** can be isolated via `pff_role = "Pass Route"` in
  pffScoutingData.csv.
- **"Openness"** can be computed from tracking `x, y` as the distance from a
  receiver to the nearest defender at (or near) the moment the ball is thrown.
- Everything keys cleanly on `gameId` + `playId` (+ `nflId` for players), so joins
  across the four tables and the per-game tracking files are straightforward.
