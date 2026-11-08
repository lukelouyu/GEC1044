# GitHub issues — complete text log

Repository: [NUS-CS2113-AY2627-S1/pe-CS2113-T10-4](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/)

Read through the signed-in Chrome session on 8 November 2026 (Asia/Singapore). All 22 issues were open; there were no closed issues. This is a cleaned transcription of the visible report text, comments, labels, and timeline, rather than a GitHub API export. Browser navigation, comment-editor controls, and other interface chrome are omitted. Embedded screenshots are not transcribed or copied; open the source issue to view them. Reports are reproduced as claims by their authors, without independent validation of the reported software behaviour.

All reports were opened by **nus-pe-bot** on **7 November 2026**, and the bot added their severity and type labels on the same date. The original interim issue reference is retained per report. Only #3 and #21 had comments or subsequent activity. Both were assigned to **officialasyrafrahim** and marked **response.Accepted**. All other issues had no assignee and no comments. All issues showed no milestone, no project, and no linked development work.

Opening times shown in Chrome (GMT+8): #1–#4 16:36; #5–#9 16:37; #10–#14 16:38; #15–#20 16:39; #21–#22 16:40. Label events for #8 and #9 were at 16:38; the other initial label events were within the same minute as opening. Chrome exposed inconsistent absolute time descriptions for the acceptance comments (the accessibility timestamp and comment action tooltip differed), so their precise time is not asserted here.

## #1 — DG: Schedule-validation diagrams give inconsistent edit-validation and duplicate-name rules

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/1)

**State:** Open. **Labels:** severity.Medium, type.DocumentationBug. **Original:** pe-interim#104.

DG: Activity schedule validation, lines 784–823, specifically:

- [Sequence source, lines 72–77](https://github.com/AY2627S1-CS2113-T10-4/tp/blob/master/docs/diagrams/atharva/sequence/ActivityScheduleValidationSequence.puml#L72-L77) and its [rendered diagram](https://github.com/AY2627S1-CS2113-T10-4/tp/blob/master/docs/images/atharva/sequence/ActivityScheduleValidationSequence.png).
- [Class source, lines 51–55](https://github.com/AY2627S1-CS2113-T10-4/tp/blob/master/docs/diagrams/atharva/class/ActivityScheduleValidatorClassDiagram.puml#L51-L55) and its [rendered diagram](https://github.com/AY2627S1-CS2113-T10-4/tp/blob/master/docs/images/atharva/class/ActivityScheduleValidatorClassDiagram.png).

### Description

The diagrams give two misleading explanations of the shared add/edit validation rules:

1. The sequence diagram says “Demand/rating-only edits skip conflict checking”, followed by “Duplicate checks always apply.” “Conflict checking” is ambiguous here: metadata-only edits still undergo duplicate checking; only the time-overlap check is skipped when the schedule is unchanged.
2. The class diagram defines duplicate names as ignoring “case/outer spaces”, omitting repeated internal whitespace. For identical dates and times, `Study group` and `study  group` are also duplicates.

The surrounding DG prose correctly states that duplicate checks always run and only actual date/time changes require fresh overlap approval. The [validator implementation, lines 40–72](https://github.com/AY2627S1-CS2113-T10-4/tp/blob/master/src/main/java/seedu/unienable/command/activity/ActivityScheduleValidator.java#L40-L72) checks normalized names before allowing the overlap check to be skipped.

### Steps to reproduce the documented mismatch

1. In a fresh test directory, with the app closed, create a UTF-8 `data/activities.txt` containing:

```text
Study group|2030-12-10|09:00|10:00|LOW|false|-|-|-
study  group|2030-12-10|09:00|10:00|LOW|false|-|-|-
```

2. Launch the app from that directory. Both saved records load without warnings.
3. Run:

```text
edit 1 imp/5
edit 1 dem/HIGH
```

Use a future date if repeating this after the sample date.

### Actual application behavior

Both metadata-only edits are rejected as duplicates of index 2, despite leaving the date and times unchanged. This demonstrates that duplicate validation still runs and repeated internal spaces do not distinguish names.

Similarly, adding a duplicate remains rejected with `overlap/ALLOW`.

### Expected documentation

The diagrams should state:

> Every edit checks duplicates. Duplicate identity requires the same date, start time, end time, and name, ignoring name case and surrounding/repeated internal whitespace. Only an actual date/time change requires fresh approval for a time overlap. `overlap/ALLOW` never permits duplicates.

Update both PlantUML sources and regenerate their rendered images.

### Impact

A maintainer could infer that metadata edits bypass validation or that internal spacing distinguishes duplicate activities. Either interpretation could lead to incorrect tests or changes to the shared add/edit contract. The diagrams should explain these rules consistently with the prose and implementation.

**Activity:** nus-pe-bot added severity.Medium and type.DocumentationBug. **Comments:** None.

## #2 — Accessible-washroom search omits CLB's recorded staff-card restriction

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/2)

**State:** Open. **Labels:** severity.Medium, type.FeatureFlaw. **Original:** pe-interim#106.

Facility feature searches show building IDs and names without the matching feature's notes. For CLB's accessible washroom, this omits a recorded staff-card restriction that affects whether a student can use the result.

### Steps to reproduce

1. Start UniEnable.
2. Enter `facility find type/ACCESSIBLE_WASHROOM`.
3. Observe that [F09] CLB appears among the facilities with status YES, without access conditions.
4. Enter `facility CLB`.
5. Compare the accessible-washroom details with the search result.

### Expected behavior

The search should include the matching feature's recorded location and access restrictions so a student can assess whether a result is usable without opening every facility separately.

### Actual behavior

The search lists CLB without its access restriction. Only the separate detail command reveals that the fourth-floor toilet requires staff-card access.

### Evidence

Search output:

```text
Facilities with ACCESSIBLE_WASHROOM (status: YES):
[F04] AS4
[F05] AS5
[F06] AS6
[F07] AS7
[F08] AS8
[F09] CLB

Sample reference data.
Verify with current campus information before you rely on it.
```

The CLB details include:

```text
ACCESSIBLE_WASHROOM | YES | 4th floor toilet requires staff card access
```

### Impact and classification

A student without a staff card may select a result before discovering its recorded restriction. Running `facility CLB` reveals the note, but the student must already know to inspect that result. Medium severity is suggested because the omitted information affects facility selection for the application's intended users, including students with mobility constraints.

**Activity:** nus-pe-bot added severity.Medium and type.FeatureFlaw. **Comments:** None.

## #3 — Priority view has no pending-only filter, leaving completed work above unfinished tasks

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/3)

**State:** Open. **Labels:** response.Accepted, severity.Medium, type.FeatureFlaw. **Assignee:** officialasyrafrahim. **Original:** pe-interim#105.

`list priority` includes completed and incomplete activities, but there is no option to show only unfinished activities in priority order. Completed high-priority work continues to appear above work that still needs attention, making the view less useful for deciding what to tackle next.

### Steps to reproduce

1. Launch UniEnable in a separate empty folder so there are no existing activities.
2. Enter:

```text
add n/Finished work d/tomorrow s/10:00 e/11:00 imp/5 urg/5 com/5
add n/Pending work d/tomorrow s/11:00 e/12:00 imp/3 urg/3 com/3
mark 1
list priority
```

### Expected behavior

Provide an option to list only incomplete activities in priority order, while retaining the existing all-activities view for reviewing completed records.

### Actual behavior

Finished work appears first with priority 250 despite being completed. Pending work appears below it with priority 54. There is no supported pending-only priority filter. The `next` command selects by start time, so it does not provide an equivalent priority ranking.

### Evidence

Recorded output:

```text
Activities by priority (highest first):
Indexes refer to the chronological 'list' order.
1. Finished work (2026-11-07, 10:00-11:00) [MEDIUM] [X] | Priority 250 (IMP 5, URG 5, COM 5)
2. Pending work (2026-11-07, 11:00-12:00) [MEDIUM] [ ] | Priority 54 (IMP 3, URG 3, COM 3)
```

### Impact and classification

As completed records accumulate, users must manually skip them to compare the priorities of unfinished tasks. Medium severity is suggested because this repeatedly complicates the planning workflow, although the completion markers still allow manual filtering.

### Activity and comment

1. nus-pe-bot added severity.Medium and type.FeatureFlaw.
2. officialasyrafrahim added response.Accepted.
3. officialasyrafrahim self-assigned the issue.
4. officialasyrafrahim commented:

> We accept this as a feature flaw with Medium severity. We reproduced the reported behaviour using the released v2.1 JAR on Java 25: the completed activity with priority 250 appears above the unfinished activity with priority 54, and there is no pending-only priority option.
>
> The existing view follows its documented scoring rules, but users planning unfinished work must manually skip completed records. This can repeatedly hinder the planning workflow as completed records accumulate, although users can continue using the completion markers. The accepted flaw is the missing filtering option, not an incorrect priority formula or a need to remove the existing all-activities view.

## #4 — Route output lacks directions needed to follow the path

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/4)

**State:** Open. **Labels:** severity.Medium, type.FeatureFlaw. **Original:** pe-interim#108.

Developer Guide user story US26 is marked implemented and states that an unfamiliar student should be able to follow a suitable path without interpreting a map. However, the route descriptions lack enough detail for one to actually navigate themselves. Example:

```text
route from/AS6 to/AS8
____________________________________________________________
Shortest recorded accessible route:
AS6 -> AS8
Total distance: 45 metres

Connections:
1. AS6 -> AS8: 45 m (Path, Sheltered)

Sample reference data.
Verify with current campus information before you rely on it.
```

There are no directions or landmarks or location notes for this connection to find one's way around without an additional map. It would be better to provide more detail.

**Activity:** nus-pe-bot added severity.Medium and type.FeatureFlaw. **Comments:** None.

## #5 — Ended activities are completely locked: cannot log an activity that already happened, and cannot even fix a typo in its name

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/5)

**State:** Open. **Labels:** severity.Low, type.FeatureFlaw. **Original:** pe-interim#243.

Steps to reproduce (use the real current date and time; replace with today's date and pick times that have already passed):

1. `add n/Morning lecture d/ s/08:00 e/09:00` (a time that has already passed today)
2. `add n/Lecture d/ s/10:00 e/11:00`
3. To get an ended activity that is in the list, add an activity that ends in a minute or two (e.g. `add n/Quick d/today s/<now+1 min> e/<now+2 min>`) and wait until it ends.
4. `edit 1 n/Quick (fixed spelling)` after it has ended.

Expected: a planner lets the user record what they actually did and correct mistakes in their own records. At the very least, fixing a name or ratings of an ended activity should work.

Actual:

- Steps 1 and 2: `[WARNING] Activities that have ended cannot be added.`
- Step 4: `[WARNING] Activities that have ended cannot be edited.` This applies to any field, not only to rescheduling.
- `edit` with a past date (`edit 3 d/2020-01-01`) gives `Edited activity must end after the current local time.`

The UG says "There is no override." The only way to fix a typo in an ended activity's name is to leave it wrong, or delete it (losing its ratings/completion state) and re-add it, which is itself impossible for a past time.

Why it is a flaw: the activity list also serves as a record (completed activities stay in `list`, `view`, and `list priority`). Locking records permanently after they end, including name/rating corrections, removes the ability to maintain that record. The user cannot log an activity they forgot to add in advance.

Severity reasoning: affects convenience of record-keeping; nothing crashes or is corrupted. Low.

Images: embedded in the source issue. Note that the first 4 commands were run at 19:11 and the next 2 commands were run at 19:20.

**Activity:** nus-pe-bot added severity.Low and type.FeatureFlaw. **Comments:** None.

## #6 — Names containing "/" such as "Lab 1/2" or "Meet w/ Prof" are rejected, and the error talks about unknown parameters

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/6)

**State:** Open. **Labels:** severity.Low, type.FeatureFlaw. **Original:** pe-interim#244.

Steps to reproduce (fresh data/ folder):

```text
add n/Lab 1/2 d/2030-04-02 s/09:00 e/10:00
add n/Read/Write lab d/2030-04-02 s/10:00 e/11:00
add n/Meet w/ Prof d/2030-04-02 s/11:00 e/12:00
add n/Q&A (CS2113), tutorial - wk#5 d/2030-04-01 s/09:00 e/10:00
```

Expected: ordinary names that students write all the time ("and/or", "w/ Prof", "Lab 1/2", "COM1/COM2", "A/B testing") can be saved.

Actual: Steps 1–3 are all rejected, e.g.:

```text
[WARNING] Unknown parameter '1/'. Valid prefixes: n/, d/, s/, e/, dem/, imp/, urg/, com/, overlap/. Use spaces or hyphens instead of literal slashes in names.
```

The message says "Unknown parameter", which describes the parser's view. It doesn't say that the user's activity name is the problem.

Characters like &, #, $, %, @, : and , are all accepted (step 4), so the restriction on "/" alone is inconsistent from the user's point of view.

The same applies to `edit INDEX n/....`.

Severity reasoning: the user can work around it by rewording, and no data is affected. Low.

Images: embedded in the source issue.

**Activity:** nus-pe-bot added severity.Low and type.FeatureFlaw. **Comments:** None.

## #7 — Command Summary in the User Guide shows stray backslashes in the command syntax

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/7)

**State:** Open. **Labels:** severity.VeryLow, type.DocumentationBug. **Original:** pe-interim#274.

### Description

In the User Guide's Command Summary table, the syntax for `add`, `edit` and `facility find` shows a backslash before each pipe, for example `d/YYYY-MM-DD\|today\|tomorrow`. The Features sections and the in-app help show the correct form without backslashes. The table is the quick reference readers copy syntax from, and a reader who types the backslash would produce an invalid command (backslashes are not accepted in names).

### Steps to reproduce

1. Open the published User Guide and go to the Command Summary table at the end.
2. Look at the rows for add, edit and facility find.

### Expected

The syntax shows the options separated by plain pipes, as elsewhere in the guide:

- `d/YYYY-MM-DD|today|tomorrow`
- `[dem/LOW|MEDIUM|HIGH]`
- `[status/YES|NO|UNKNOWN]`

### Actual

The syntax shows `\|` between the options:

- `d/YYYY-MM-DD\|today\|tomorrow` (in the add and edit rows)
- `[dem/LOW\|MEDIUM\|HIGH]` (in the add and edit rows)
- `[status/YES\|NO\|UNKNOWN]` (in the facility find row)

### Severity justification

VeryLow: it is a formatting problem in the documentation (stray escape characters in a table). The correct syntax appears in the Features sections and in the in-app help, so it does not stop a reader from using the app.

**Activity:** nus-pe-bot added severity.VeryLow and type.DocumentationBug. **Comments:** None.

## #8 — A missed (ended) activity cannot be corrected or rescheduled, so the only way to fix it is to delete and re-add it

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/8)

**State:** Open. **Labels:** severity.Low, type.FeatureFlaw. **Original:** pe-interim#275.

### Description

The `overdue` command is meant to help users recover from missed activities, but every edit to an ended activity is refused: fixing a typo in the name, changing a rating, or moving it to a later date. The warning gives no suggestion about what to do instead. The only way out is to delete the activity and re-add it, retyping its date, times and ratings. For the target users, missing or mistiming an activity is a normal event, so the feature does not complete its own purpose of helping them catch up.

### Steps to reproduce

1. In an empty folder, create `data/activities.txt` containing exactly one line:

```text
Physio appt typo|2026-11-05|09:00|10:00|HIGH|false|5|4|5
```

(In PowerShell: `mkdir data` then `Set-Content -Path data\activities.txt -Value 'Physio appt typo|2026-11-05|09:00|10:00|HIGH|false|5|4|5'`.)

2. Start the app: `java -jar CS2113-T10-4-UniEnable.jar`.
3. Enter, one per line:

```text
list
overdue
edit 1 n/Physio appointment
edit 1 imp/4
edit 1 d/tomorrow
```

### Expected

A missed activity can be corrected or rescheduled, or the message tells the user what to do instead.

### Actual

`overdue` lists the activity, and all three edit commands are refused with the same warning and no next step:

```text
1. [OVERDUE WEEK] Physio appt typo (2026-11-05, 09:00-10:00) [HIGH] [ ]
[WARNING] Activities that have ended cannot be edited.
[WARNING] Activities that have ended cannot be edited.
[WARNING] Activities that have ended cannot be edited.
```

### Severity justification

Low: the behaviour is documented and a workaround exists (delete and re-add), so it is a minor inconvenience, but it works against the main purpose of the overdue feature for the target users.

**Activity:** nus-pe-bot added severity.Low and type.FeatureFlaw. **Comments:** None.

## #9 — Non-English activity names are saved as question marks instead of being rejected on a Windows console

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/9)

**State:** Open. **Labels:** severity.Low, type.FunctionalityBug. **Original:** pe-interim#276.

### Description

The User Guide (Adding an activity, and the Error Handling table with the example `add n/Café ...`) says an activity name containing non-English characters is rejected with "Please write the activity name in English (ASCII characters only)". On a Windows console using the older default code page (437), no warning is shown. The non-ASCII characters are replaced with `?` before the app validates them, so a name such as `?????` passes the ASCII check and is saved. The original name is permanently lost. The User Guide's Quick Start does not mention setting the console to UTF-8.

### Steps to reproduce

1. On Windows, open Command Prompt or PowerShell and run `chcp`. If the result is not 437, run `chcp 437`.
2. In an empty folder (no existing data folder), start the app: `java -jar CS2113-T10-4-UniEnable.jar`.
3. Enter, one per line (paste them if your keyboard cannot type Hindi):

```text
add n/हिंदी d/2026-12-11 s/09:00 e/10:00
add n/परीक्षा तैयारी d/2026-12-12 s/09:00 e/10:00
list
bye
```

### Expected

Both add commands show:

```text
[WARNING] Please write the activity name in English (ASCII characters only).
```

and list shows no activities.

### Actual

Both activities are added with question-mark names. The first add prints:

```text
Added activity: ?????
Date: 2026-12-11
Time: 09:00 - 10:00
Demand: MEDIUM
```

and list shows:

```text
1. ????? (2026-12-11, 09:00-10:00) [MEDIUM] [ ]
2. ??????? ?????? (2026-12-12, 09:00-10:00) [MEDIUM] [ ]
```

### Severity justification

Low: it only affects users who type non-ASCII text on a Windows console using a non-UTF-8 code page, and the rest of the app works normally. It is more than cosmetic because an incorrect name is saved.

**Activity:** nus-pe-bot added severity.Low and type.FunctionalityBug. **Comments:** None.

## #10 — Two running instances overwrite each other’s saved data and the User Guide does not warn about it

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/10)

**State:** Open. **Labels:** severity.Low, type.DocumentationBug. **Original:** pe-interim#277.

### Description

If UniEnable is started twice from the same folder, each running copy keeps its own list in memory and saves its whole list on every change, so the second copy silently overwrites the first copy's changes. The User Guide (Data Storage section) never tells users to run only one copy per data folder. Only the Developer Guide mentions this limit.

### Steps to reproduce

1. Open two terminals (A and B) in the same empty folder and run `java -jar CS2113-T10-4-UniEnable.jar` in both. Leave both running.
2. In terminal A, enter: `add n/FromA d/2026-12-10 s/09:00 e/10:00`.
3. In terminal B, enter: `add n/FromB d/2026-12-10 s/09:00 e/10:00`. (No clash warning appears, although terminal A already booked this slot.)
4. In terminal A, enter: `add n/FromA2 d/2026-12-10 s/13:00 e/14:00`.
5. In terminal B, enter: `mark 1`.
6. Enter `bye` in terminal A, then `bye` in terminal B.
7. In the folder, run `type data\activities.txt` (or open the file).

### Expected

The User Guide warns that only one copy of the app should be run per data folder, so users know to avoid this.

### Actual

The User Guide has no such warning. No warning was shown in either terminal. The saved file contains only the second copy's data:

```text
FromB|2026-12-10|09:00|10:00|MEDIUM|true|-|-|-
```

FromA and FromA2 are permanently lost.

### Severity justification

Low: it needs an unusual action (running two copies at once), so it appears only in rare situations. It is not purely cosmetic because of the data loss.

**Activity:** nus-pe-bot added severity.Low and type.DocumentationBug. **Comments:** None.

## #11 — Help-error table in the User Guide renders as raw pipe-delimited text

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/11)

**State:** Open. **Labels:** severity.VeryLow, type.DocumentationBug. **Original:** pe-interim#335.

### Location

UniEnable v2.1 User Guide, Error Handling, immediately after “For help-command errors, check the response below and enter a single valid topic.”

[User Guide — Error Handling](https://ay2627s1-cs2113-t10-4.github.io/tp/UserGuide.html#error-handling)

### Steps to reproduce

1. Open the User Guide in a browser.
2. Search for `Help input problem`.
3. Inspect the help-error information below the introductory sentence.

### Actual result

The intended three-column table is displayed as a continuous paragraph containing literal `|` separators and separator dashes. The headings, the `help extra` example, and the `help add extra` example run together instead of appearing in separate rows and columns. The surrounding error-handling tables render normally.

### Expected result

Render a table with three columns (Help input problem, Example input, Expected response) and a separate row for each example, or use an equivalently clear list.

### Impact

The information is still readable, but the broken formatting makes it harder to match an example command to its expected response. This is a cosmetic documentation defect; VeryLow is proposed. It does not prevent the help command from working.

Screenshot embedded in the source issue.

**Activity:** nus-pe-bot added severity.VeryLow and type.DocumentationBug. **Comments:** None.

## #12 — Ordinary English activity names containing a typographic apostrophe are rejected

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/12)

**State:** Open. **Labels:** severity.VeryLow, type.FeatureFlaw. **Original:** pe-interim#336.

### Environment

Supplied CS2113-T10-4-UniEnable.jar (v2.1), Windows, Oracle Java 25.0.1. Reproduced on 6 November 2026 and rechecked on 7 November 2026.

### Problem

The printable-ASCII restriction rejects ordinary English activity names containing a typographic apostrophe (’, U+2019). Such punctuation commonly appears in copied appointment titles or prose. The application asks the user to write the name in English even though the name is already English.

The UG documents the ASCII limitation. This report challenges the over-restrictive input design for otherwise ordinary English names, not the consistency between the UG and the implementation.

### Steps to reproduce

1. Launch the supplied JAR in a fresh working directory.
2. Copy and enter the following command, retaining the curved apostrophe:

```text
add n/Tutor’s consultation d/tomorrow s/10:00 e/11:00
```

3. Enter the otherwise identical command using a straight ASCII apostrophe:

```text
add n/Tutor's consultation d/tomorrow s/10:00 e/11:00
```

4. Enter `list`.

### Actual result

The first command is rejected:

```text
[WARNING] Please write the activity name in English (ASCII characters only).
```

The second command succeeds. There is no date, overlap or duplicate issue; changing only the punctuation determines whether the name is accepted.

### Expected result

Accept ordinary typographic apostrophes in English activity names, or normalize them to their ASCII equivalent, while continuing to reject characters that interfere with the command or storage format.

### Impact and severity

A user copying a normal English title must identify and replace punctuation before the activity can be recorded. This is a small, recoverable inconvenience, so VeryLow is proposed. The application already supports UTF-8 stored names; this report does not request full multilingual UI support or arbitrary control characters.

**Activity:** nus-pe-bot added severity.VeryLow and type.FeatureFlaw. **Comments:** None.

## #13 — Overdue incomplete activities cannot be rescheduled through edit

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/13)

**State:** Open. **Labels:** severity.Medium, type.FeatureFlaw. **Original:** pe-interim#337.

### Environment

- Application: supplied CS2113-T10-4-UniEnable.jar (v2.1)
- Operating system: Windows
- Java: 25

### Summary

An activity becomes entirely uneditable once its original end time passes, even when it remains incomplete and the requested replacement date is in the future.

Consequently, a student who misses a planned study session cannot use edit to move that unfinished activity to tomorrow. They must recreate the activity and deal with the old overdue record separately.

The User Guide explicitly documents that ended activities cannot be edited. This report concerns the usefulness of that restriction for normal planning, rather than a mismatch between the implementation and the User Guide.

### Steps to reproduce

1. Use a fresh working directory.
2. Before launching the application, create `data/activities.txt` containing the following valid record. Replace YESTERDAY with yesterday's local date in YYYY-MM-DD format:

```text
Prepare tutorial|YESTERDAY|09:00|10:00|HIGH|false|5|4|3
```

This represents an activity saved previously that was not completed before its scheduled end. Loading past activities is supported by the application.

3. Launch the supplied JAR from that working directory.
4. Enter `overdue`.
5. Confirm that Prepare tutorial appears as an incomplete overdue activity with index 1.
6. Attempt to move it to tomorrow: `edit 1 d/tomorrow`.
7. Enter `list`.

### Actual result

The edit is rejected with:

```text
[WARNING] Activities that have ended cannot be edited.
```

The subsequent list output shows that the activity remains incomplete and retains its original date.

The application rejects the operation even though the requested new schedule is in the future and there are no other activities that could cause an overlap or duplicate.

### Expected result

Allow an incomplete overdue activity to be rescheduled to a valid future date or time.

The resulting schedule should still pass the existing time, duplicate and overlap checks. Fields omitted from the edit, such as the name, demand and ratings, should be preserved.

### Impact and severity

Rescheduling unfinished work after missing a planned time block is a normal workflow for a student planning application, particularly one aimed partly at students with ADHD.

The existing overdue command helps users identify unfinished activities, but those activities cannot then be rescheduled using the existing edit command. The workaround requires manually recreating the name, schedule, demand and ratings, followed by separately deleting the old record or leaving it in the overdue list. This adds unnecessary steps and creates opportunities to omit details during re-entry.

I propose severity.Medium: some users will encounter this during normal planning and experience repeated inconvenience, but they can continue using the application through the delete-and-recreate workaround.

Screenshots embedded in the source issue.

**Activity:** nus-pe-bot added severity.Medium and type.FeatureFlaw. **Comments:** None.

## #14 — Calendar row numbers can cause deletion of a different activity without an on-screen warning

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/14)

**State:** Open. **Labels:** severity.Medium, type.FeatureFlaw. **Original:** pe-interim#338.

### Environment

- Application: supplied CS2113-T10-4-UniEnable.jar (v2.1)
- Operating system: Windows
- Java: 25

### Summary

Calendar dashboards display period-local row numbers, but commands such as delete interpret indexes using the full chronological activity list. The dashboard does not display a warning explaining that its numbers cannot be used directly with these commands.

As a result, a user who checks tomorrow's schedule and then deletes an activity using the number displayed beside it can delete a different activity that is not visible in the dashboard.

The User Guide documents this numbering distinction and advises running list. This report concerns the usability of the numbering design, rather than a mismatch between the implementation and the User Guide.

### Steps to reproduce

1. Use a fresh working directory.
2. Before launching the application, create `data/activities.txt` with the following two valid records. Replace YESTERDAY and TOMORROW with the corresponding local dates in YYYY-MM-DD format:

```text
Earlier lecture|YESTERDAY|22:00|23:00|MEDIUM|false|-|-|-
Tomorrow consultation|TOMORROW|10:00|11:00|MEDIUM|false|-|-|-
```

These records represent an existing earlier activity and an activity scheduled for tomorrow. They use the application's supported storage format.

3. Launch the supplied JAR from that working directory.
4. Enter `view tomorrow`.
5. Observe that Tomorrow consultation is displayed with row number 1.
6. Enter `delete 1`.
7. Enter `list`.

### Actual result

The calendar displays Tomorrow consultation as row 1:

```text
1. 10:00-11:00 [ ] Tomorrow consultation
```

However, delete 1 reports:

```text
Deleted activity: Earlier lecture
```

The subsequent list output still contains Tomorrow consultation, while Earlier lecture has been removed.

The dashboard does not warn that its row numbers differ from the indexes accepted by modifying commands. The deletion happens without asking the user to confirm the identity of the activity.

### Expected result

Calendar dashboards should display the same actionable chronological indexes used by the other activity views.

Alternatively, if period-local numbering is retained, the dashboard should clearly distinguish these numbers from activity indexes and explicitly instruct the user to obtain the correct index before modifying an activity.

### Impact and severity

Checking tomorrow's schedule and then changing an entry is a normal planning workflow. The inconsistent numbering can cause a user to delete an unrelated commitment that was not displayed in the current view.

This situation can arise whenever earlier activities exist outside the selected calendar period. It does not require malformed data or an extreme input. Other filtered views, such as find, retain chronological indexes, making the calendar's different behaviour easy to overlook.

I propose severity.Medium: the issue can cause occasional unintended deletion, but users who remember to run list before making changes can continue using the application.

Screenshots embedded in the source issue.

**Activity:** nus-pe-bot added severity.Medium and type.FeatureFlaw. **Comments:** None.

## #15 — DG: Model overview incorrectly states that every displayed index uses canonical ordering

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/15)

**State:** Open. **Labels:** severity.Low, type.DocumentationBug. **Original:** pe-interim#404.

DG (Model section): L166-L171.

### Description

The model overview describes the canonical view as:

> “the one ordering that every displayed index refers to”

This incorrectly includes calendar dashboards. The Calendar dashboards section, lines 366–367 and Displayed index glossary entry, line 1229 explain that dashboards number activities within the selected period, while indexed change commands use the full chronological list.

### Example

Suppose list contains:

| Canonical index | Activity |
| --- | --- |
| 1 | Today work |
| 2 | Tomorrow class |

`view tomorrow` displays Tomorrow class as row 1. However, an indexed change targeting 1 still refers to Today work.

The dashboard therefore displays a number that does not refer to the activity’s canonical index.

### Expected documentation

The overview should distinguish canonical indexes from dashboard row numbers. Suggested wording:

> The canonical view orders activities by date, start time, and insertion order for ties. It defines the indexes used by indexed change commands and retained by list-based query views. Calendar dashboards use separate row numbering within the selected period.

### Impact

The overview gives developers an incorrect global invariant. A maintainer could assume that a dashboard row number is an actionable list index, leading to incorrect command handling or tests. Later sections explain the exception, but the overview should state it directly.

**Activity:** nus-pe-bot added severity.Low and type.DocumentationBug. **Comments:** None.

## #16 — Unfinished overdue activities cannot be rescheduled to a future date

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/16)

**State:** Open. **Labels:** severity.Medium, type.FeatureFlaw. **Original:** pe-interim#405.

Once an activity has ended, all edits are blocked, including moving an unfinished activity to a valid future slot. This prevents a student from postponing a missed study or assignment session while keeping the same record and its details.

### Steps to reproduce

1. Use a separate test launch folder. With UniEnable closed, create its `data/activities.txt` as a UTF-8 file containing this single row:

```text
Missed submission|2026-11-05|10:00|11:00|HIGH|false|5|5|5
```

2. Ensure that the saved date is before today's local date. The recorded test used 5 November 2026; substitute yesterday's date in YYYY-MM-DD format when reproducing on another date.
3. Start UniEnable from that folder and enter:

```text
overdue
edit 1 d/tomorrow
list
```

### Expected behavior

An incomplete overdue activity should be reschedulable to a valid future date and time, subject to the usual duplicate and overlap checks, while preserving its other fields.

### Actual behavior

`overdue` correctly identifies the unfinished activity, but the edit is rejected because its original schedule has ended. Its date remains unchanged.

### Evidence

Relevant output from the recorded session:

```text
Overdue activities (ended before now):
1. [OVERDUE WEEK] Missed submission (2026-11-05, 10:00-11:00) [HIGH] [ ]
```

The edit returns:

```text
[WARNING] Activities that have ended cannot be edited.
```

The subsequent list still contains:

```text
1. Missed submission (2026-11-05, 10:00-11:00) [HIGH] [ ]
```

### Impact and classification

The user must recreate the activity and its fields, then remove the old entry, or edit the saved file outside the application. Medium severity is suggested because this blocks a normal rescheduling workflow even though a workaround exists.

**Activity:** nus-pe-bot added severity.Medium and type.FeatureFlaw. **Comments:** None.

## #17 — Developer Guide sequence diagrams use open arrowheads for method calls; the course convention is filled arrowheads for synchronous calls

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/17)

**State:** Open. **Labels:** severity.Low, type.DocumentationBug. **Original:** pe-interim#517.

Where: [Developer Guide](https://ay2627s1-cs2113-t10-4.github.io/tp/DeveloperGuide.html), all sequence diagrams. Examples to open: TopicHelpSequence and EditActivitySequence (images under `docs/images/atharva/sequence/` and `docs/images/oliver/sequence/`).

Problem: in every sequence diagram I opened, synchronous method calls (e.g. `execute(activities, storage)`, `parse("help view")`, `showMessage(...)`) end in an open "V"-shaped (lined) arrowhead. The course textbook (Modeling -> UML Sequence Diagrams -> Basic Notation) says synchronous calls use filled arrowheads, and lined arrowheads are for asynchronous calls. Calls in these diagrams are plain Java calls, so the filled style is the correct one. As drawn, the diagrams say every call is asynchronous.

Evidence: zoom into the arrow after the label `execute(activities, storage)` in TopicHelpSequence.png or DeleteActivitySequence.png: the head is two thin lines, not a filled triangle. All 20 sequence diagrams are generated from the same style (PlantUML `->` arrows with the shared skinparam block).

Severity reasoning: the DG is still readable, but it's a notation error affecting every sequence diagram. Low.

**Activity:** nus-pe-bot added severity.Low and type.DocumentationBug. **Comments:** None.

## #18 — Wrong error message for a date written with slashes: it blames the activity name

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/18)

**State:** Open. **Labels:** severity.VeryLow, type.FunctionalityBug. **Original:** pe-interim#518.

Steps to reproduce (fresh data/ folder):

```text
add n/Study d/2030/03/12 s/09:00 e/10:00
add n/Study d/2030-3-12 s/09:00 e/10:00
```

Expected: a message that the date is invalid and shows the expected form (YYYY-MM-DD), like the one in step 2.

Actual:

Step 2 prints `[WARNING] Invalid date. Use a real YYYY-MM-DD date, today, or tomorrow.`, which is helpful.

Step 1 prints:

```text
[WARNING] Unknown parameter '2030/'. Valid prefixes: n/, d/, s/, e/, dem/, imp/, urg/, com/, overlap/. Use spaces or hyphens instead of literal slashes in names.
```

The user typed a date, not a name, so the tip about names is irrelevant, and the date format is never mentioned. Writing `12/03/2030` or `2030/03/12` is a very common user mistake.

A similar thing happens when the space between two fields is missing (`d/2030-03-07s/09:00`): the same "slashes in names" advice appears.

Severity reasoning: only a misleading message; the command is correctly rejected and nothing is changed. VeryLow.

Images embedded in the source issue.

**Activity:** nus-pe-bot added severity.VeryLow and type.FunctionalityBug. **Comments:** None.

## #19 — Dashboard (view) rows are numbered from 1 per period, so using them with delete/edit/mark silently hits a different activity

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/19)

**State:** Open. **Labels:** severity.Low, type.FeatureFlaw. **Original:** pe-interim#520.

Steps to reproduce (fresh data/ folder; do this before 23:00 local time. Run it on the day you file, since it uses d/today):

```text
add n/Gym today d/today s/23:00 e/23:30
add n/Tutorial prep d/tomorrow s/09:00 e/10:00
add n/Project meeting d/tomorrow s/14:00 e/15:00
```

`list` shows: 1 Gym today, 2 Tutorial prep, 3 Project meeting.

`view tomorrow` shows the schedule rows as `1. 09:00-10:00 Tutorial prep` and `2. 14:00-15:00 Project meeting`.

The user wants to remove "Tutorial prep" and types `delete 1` using the dashboard row number.

Expected: a number shown next to an activity should be usable with the commands that take an INDEX. Or the dashboard should not show a number that can be mistaken for one. Or destructive commands should show enough of a confirmation to catch the mistake.

Actual:

- `delete 1` deletes "Gym today" (list index 1). It prints `Deleted activity: Gym today.`
- The user's intended activity is still there.
- There is no confirmation prompt and no undo (`help delete` says "There is no undo command").
- The same applies to `edit N` and `mark N`, which silently change the wrong activity.

Why it is a flaw: the row numbers have the same look and position as list indexes, and they agree whenever the period starts at the first activity. So the user's habit is reinforced until the day they differ. After a mistaken delete the data is gone.

Severity reasoning: needs a user mistake, but the consequence is irreversible deletion of a user's own data. I'm not claiming Medium because the documentation warns about it. Low is the conservative choice.

Images embedded in the source issue.

**Activity:** nus-pe-bot added severity.Low and type.FeatureFlaw. **Comments:** None.

## #20 — find only matches an exact contiguous phrase, so searching "group study" or "tutorial wk" finds nothing

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/20)

**State:** Open. **Labels:** severity.Low, type.FeatureFlaw. **Original:** pe-interim#519.

Steps to reproduce (fresh data/ folder, v1 JAR):

1. Run the JAR.
2. `add n/Study Group d/2030-01-08 s/09:00 e/10:00`
3. `add n/Q&A (CS2113), tutorial - wk#5 d/2030-01-09 s/09:00 e/10:00`
4. `find group study`
5. `find tutorial wk`
6. `find study group` (control)

Expected: a user who types the words they remember from a name (in any order) gets the activity back, or at least a hint that the words must form one exact phrase. Search is the main way to locate an index for edit/mark/delete.

Actual:

- Step 4 prints `Sorry, no activity names match your search.`
- Step 5 prints the same, even though both words appear in the second activity's name.
- Only step 6 (exact phrase, same order) finds anything.
- The no-match message does not say that multi-word keywords are matched as one phrase.

Why it is a flaw: users normally remember keywords, not the exact wording of a name. The only feedback is "no match", so they may conclude the activity does not exist, and then add a duplicate or give up.

Severity reasoning: the feature still works for single words and exact phrases, and nothing is lost or corrupted. Inconvenience only, so Low rather than Medium.

Images embedded in the source issue.

**Activity:** nus-pe-bot added severity.Low and type.FeatureFlaw. **Comments:** None.

## #21 — List priority ranks an activity with a missing rating below the least important fully rated activity

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/21)

**State:** Open. **Labels:** response.Accepted, severity.Low, type.FeatureFlaw. **Assignee:** officialasyrafrahim. **Original:** pe-interim#540.

### Description

The User Guide invites users to give all, some or none of the importance, urgency and commitment ratings. In `list priority`, an activity with only some ratings gets Priority NA and is placed after every fully rated activity, even one with the lowest possible score. A user who rates an important task with importance 5 and urgency 5 but leaves out commitment sees it ranked below a trivial task rated 1/1/1. The command exists to help decide what to do first, so this misleads the user, and no warning mentions that the missing rating is the reason.

### Steps to reproduce

1. In an empty folder, start the app: `java -jar CS2113-T10-4-UniEnable.jar`.
2. Enter, one per line:

```text
add n/Assignment due d/2026-12-09 s/20:00 e/21:00 imp/5 urg/5
add n/Tidy desk d/2026-12-10 s/20:00 e/20:15 imp/1 urg/1 com/1
list priority
```

### Expected

The assignment is not ranked below the lowest possible score, or the app warns the user that a rating is missing.

### Actual

```text
Activities by priority (highest first):
2. Tidy desk (2026-12-10, 20:00-20:15) [MEDIUM] [ ] | Priority 2 (IMP 1, URG 1, COM 1)
1. Assignment due (2026-12-09, 20:00-21:00) [MEDIUM] [ ] | Priority NA (IMP 5, URG 5, COM -)
```

The tidy-desk task is ranked first and the assignment last. No warning says that the missing commitment rating is the reason.

### Severity justification

Low: the behaviour is documented and only affects users who rate some but not all fields, so it is a minor inconvenience, but it works against the purpose of the command.

### Activity and comment

1. nus-pe-bot added severity.Low and type.FeatureFlaw.
2. officialasyrafrahim added response.Accepted.
3. officialasyrafrahim self-assigned the issue.
4. officialasyrafrahim commented:

> We accept this as a feature flaw with Low severity. We reproduced the reported ordering using the released v2.1 JAR on Java 25: an activity rated IMP 5 and URG 5 without COM appears as Priority NA below a fully rated activity with priority 2.
>
> This follows the documented rule that all three ratings are needed to calculate a score. The NA value and missing-field marker provide some indication, so we are not treating the calculation as mathematically incorrect. However, partial ratings are supported, and clearer in-app explanation that the missing rating prevents scoring, with guidance to supply it, would make the priority view more useful. The inconvenience is limited to partially rated activities and users can continue using the application.

## #22 — When saving fails, the app shows no cause and does not show the result of the command

[Source issue](https://github.com/NUS-CS2113-AY2627-S1/pe-CS2113-T10-4/issues/22)

**State:** Open. **Labels:** severity.Low, type.FunctionalityBug. **Original:** pe-interim#541.

### Description

When saving to `data/activities.txt` fails, the app prints only `Unable to save activities: data\activities.txt`. It does not say why the save failed, the line has no `[WARNING]` prefix like the other warnings, and the normal confirmation for the command (for example `Added activity: New`) is not shown even though the change was applied in memory. The unsaved-changes warning tells the user to "Fix the save error", but no reason is given, so the user cannot tell what to fix, or whether the add succeeded.

### Steps to reproduce (Windows)

1. In an empty folder, start the app (`java -jar CS2113-T10-4-UniEnable.jar`), enter `add n/First d/2026-12-20 s/09:00 e/10:00`, then enter `bye`.
2. In a separate terminal (not inside the app), in the same folder, run: `attrib +r data\activities.txt`.
3. Start the app again and enter: `add n/New d/2026-12-21 s/09:00 e/10:00`.
4. Enter `list`.

### Expected

A warning that names the problem (for example that the file is read-only), and the usual confirmation `Added activity: New` with its details, because the change was made in memory.

### Actual

Only the following is shown after the add, with no cause and no `Added activity: New` confirmation:

```text
Unable to save activities: data\activities.txt
[WARNING] Unsaved activity changes. Fix the save error and enter 'bye' to retry saving and exit.
To quit without saving these changes, end input with Ctrl+D (Windows: Ctrl+Z, then Enter).
```

`list` then shows that New is in memory:

```text
1. First (2026-12-20, 09:00-10:00) [MEDIUM] [ ]
2. New (2026-12-21, 09:00-10:00) [MEDIUM] [ ]
```

### Severity justification

Low: save failures are rare and the app keeps the data in memory, so this is only a minor inconvenience. It is more than cosmetic because the user is told to fix an error without being told what the error is.

**Activity:** nus-pe-bot added severity.Low and type.FunctionalityBug. **Comments:** None.
