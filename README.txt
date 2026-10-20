================================================================================
                    P25 GYM MEMBERSHIP MANAGER
================================================================================

Student Name     : Saadhana Durga S
Register Number  : 7376252IT316
Degree & Branch  : B.Tech Information Technology (Second Year)
Course / Project : Terminal-Based Python Project — P25 Gym Membership Manager
Submission Date  : October 2026

================================================================================
1. PROJECT TITLE
================================================================================
P25 Gym Membership Manager: A Terminal-Based Membership, Attendance, and
Revenue Management System in Pure Python.


================================================================================
2. PROJECT OBJECTIVE
================================================================================
The objective of this project is to provide a lightweight, robust, and
dependency-free terminal application for fitness center owners and front-desk
staff. The system automates gym member enrollment, fee collection tracking,
membership validity and renewals, daily check-in logging, expiry alerts,
membership freezes, personal trainer assignments, and monthly financial
reporting using persistent plain-text file storage.


================================================================================
3. PROBLEM STATEMENT
================================================================================
Small and mid-sized gym facilities often struggle with manual paper logbooks
or complicated spreadsheet templates. Paper logs lead to uncollected renewal fees,
overlooked expired memberships, slow check-in lookups, and inaccurate revenue
calculations.

Commercial fitness management software is frequently costly, requires dedicated
database servers, or demands internet connectivity. The P25 Gym Membership
Manager solves this problem by delivering a robust, automated command-line system
built entirely with foundational Python concepts, requiring zero external
dependencies or database engines.


================================================================================
4. MAIN FEATURES & BONUS IMPLEMENTATION
================================================================================
A. REQUIRED FEATURES (OPTIONS 1 TO 8):
- Fast Member Registration: Automatically assigns incremental, collision-free
  member IDs (e.g., G0001, G0002) and computes plan-specific expiration dates.
- Tabular Member Directory: Displays registered members in an aligned,
  easy-to-read terminal table.
- Seamless Membership Renewal: Detects whether a member is currently active or
  expired. For active members, the new plan extends from their existing expiry
  date; for expired members, the renewal begins from the session date.
- Proactive Expiry Alerts: Identifies memberships that have already lapsed,
  expire today, or will expire within the next 7 days.
- Daily Check-in Verification: Validates active membership status prior to
  recording attendance; expired members are refused entry.
- Monthly Attendance Counter: Tallies attendance records for any selected member,
  month, and year (accepting both single-digit '8' and two-digit '08' inputs).
- Revenue & Active Member Reporting: Aggregates revenue strictly from payment
  transaction records and breaks down active members across all four plans.
- Error Tolerance & Clean Exit: Safely ignores corrupted lines, empty lines, and
  missing data files without crashing, and terminates cleanly on option 8.

B. OPTIONAL BONUS FEATURES (OPTIONS 9 AND 10):
- Bonus A (Option 9) - Membership Freeze:
  Allows an active membership to be frozen for up to 15 days, extending the
  member's expiry date using pure calendar day arithmetic (handling month
  and year rollovers and leap years). Rejects freeze requests for expired
  members and strictly prevents freeze requests exceeding the 15-day limit.
- Bonus B (Option 10) - Personal Trainer Assignment:
  Allows members to be assigned or reassigned to certified personal trainers.
  Enforces a strict maximum capacity of 10 members per trainer, displays trainer
  rosters with real-time availability, and prevents double-counting upon reassignment.


================================================================================
5. MEMBERSHIP PLANS AND PRICING
================================================================================
The system supports exactly four membership plans:

+----------------+--------------+---------------+
| Plan Name      | Duration     | Fee (INR)     |
+----------------+--------------+---------------+
| Monthly        | 1 month      | Rs. 1,200     |
| Quarterly      | 3 months     | Rs. 3,300     |
| Half-yearly    | 6 months     | Rs. 6,000     |
| Annual         | 12 months    | Rs. 10,800    |
+----------------+--------------+---------------+

The application allows users to choose plans by either option number (1 to 4)
or by plan name (case-insensitive, e.g., 'Monthly' or 'monthly').


================================================================================
6. TECHNOLOGIES AND PYTHON CONCEPTS USED
================================================================================
Strictly adheres to faculty guidelines with ZERO external libraries or imports:
- No 'datetime', 'os', 'sys', 'math', 'json', 'csv', 'random', 're', or third-party packages.
- Zero 'eval()' or 'exec()' usage.
- Variables and constants (all limits and prices defined as uppercase constants).
- Modular architecture with every user-defined function strictly <= 40 lines.
- Data structures: Lists, dictionaries, tuples, and sets.
- Control flow: 'if', 'elif', 'else', 'for', and 'while' loops.
- Custom date validation, leap-year calculations, and month-end clamping.
- Pure Python day-addition algorithm crossing month/year boundaries for freezes.
- Exception handling: 'try' and 'except FileNotFoundError', 'ValueError'.
- File handling: Built-in 'open()' using context managers ('with' statement).
- String processing: 'split()', 'strip()', 'upper()', 'lower()', 'isdigit()',
  'replace()', 'startswith()', and f-strings.
- Terminal formatting: Fixed-width string formatting for tabular output.


================================================================================
7. DESCRIPTION OF PROJECT FILES
================================================================================
The submission folder '7376252IT316_P25' contains exactly six files:
- main.py        : Complete Python application containing date arithmetic,
                   file persistence functions, menu navigation, and reporting.
- members.txt    : Persistent text database of gym members.
- payments.txt   : Persistent audit log of all financial transactions (new
                   registrations and renewals).
- checkins.txt   : Persistent log of daily attendance check-ins.
- README.txt     : Project documentation and user manual.
- sample_run.txt : Realistic terminal execution transcript demonstrating all
                   ten menu options and comprehensive error handling.


================================================================================
8. STORAGE FORMAT EXPLANATION
================================================================================
All data files use plain text (.txt) with pipe-delimited (|) fields.
Each record occupies exactly one line.

1. members.txt
   Standard Format: MemberID|Name|Phone|Plan|StartDate|ExpiryDate
   Extended Format: MemberID|Name|Phone|Plan|StartDate|ExpiryDate|TrainerID|FreezeDays
   Example (standard): G0001|Saadhana Durga|9876543210|Monthly|19-10-2026|19-11-2026
   Example (bonus)   : G0004|Arun Kumar|9123456780|Annual|10-01-2026|17-01-2027|T01|7
   Note: Standard 6-field lines are automatically parsed with default 'Unassigned'
   trainer and '0' freeze days, ensuring 100% backward and forward compatibility.

2. payments.txt
   Format: MemberID|Date|Plan|Amount
   Example: G0001|19-10-2026|Monthly|1200

3. checkins.txt
   Format: MemberID|Date
   Example: G0001|19-10-2026


================================================================================
9. HOW TO RUN THE PROGRAM
================================================================================
Follow these steps:
1. Open terminal in the project directory:
   cd "7376252IT316_P25"
2. Run the application:
   python main.py
3. Enter today's date in DD-MM-YYYY format when requested (e.g., 19-10-2026).
4. Follow the displayed menu options (1 to 10).


================================================================================
10. HOW TO USE EACH MENU OPTION
================================================================================
1. Register member:
   Prompts for member's full name, 10-digit phone number, and plan. Uses
   the validated session date as join date, computes expiry date, generates
   unique ID (e.g., G0013), and appends records to members.txt and payments.txt.

2. View all members:
   Renders an aligned table displaying all registered members with their ID,
   name, phone, plan, joining date, and expiry date.

3. Renew membership:
   Prompts for Member ID, displays current details, and checks active status.
   If active (expiry date >= today), duration is added to current expiry date;
   if expired, it is added to the session date. Records payment in payments.txt.

4. Show expiry alerts:
   Displays two lists based on the session date:
   - Already Expired: Memberships whose expiry date is strictly before today.
   - Expiring Today / Soon: Memberships expiring today (day 0) or within the
     next 7 days.

5. Record daily check-in:
   Prompts for Member ID. If active (expiry date >= today), records check-in
   in checkins.txt. If expired, check-in is refused.

6. Count monthly check-ins:
   Prompts for Member ID, month (1-12, accepting both '8' and '08'), and
   year (YYYY). Counts and displays visits in that month.

7. Monthly revenue and active member report:
   Prompts for month and year. Calculates revenue strictly from payment
   records dated in that month, then reports active members categorized
   across all four plans (Monthly, Quarterly, Half-yearly, Annual).

8. Exit:
   Displays a friendly goodbye message and cleanly terminates the loop.

9. Freeze membership (Bonus A):
   Prompts for Member ID. Verifies active membership. Prompts for freeze
   duration (1-15 days, tracking previously used freeze days so total cannot
   exceed 15 days). Extends expiry date in members.txt using pure calendar math.

10. Assign personal trainer (Bonus B):
    Displays trainer roster with current assignments and capacities. Prompts
    for Member ID and Trainer ID (T01, T02, T03). Enforces strict maximum of
    10 members per trainer. Handles reassignment seamlessly without double-counting.


================================================================================
11. DATE ARITHMETIC ALGORITHMS (ZERO IMPORTS)
================================================================================
- Strict format: DD-MM-YYYY (2-digit day, 2-digit month, 4-digit year).
- Rejects impossible dates (e.g., 31-02-2026, 00-12-2026, 15-13-2026).
- Full Gregorian leap-year algorithm:
  * A year divisible by 400 is a leap year.
  * A year divisible by 100 but not 400 is NOT a leap year.
  * A year divisible by 4 but not 100 is a leap year.
- Month-end date arithmetic (add_months):
  Adding 1 month to 31-01-2026 produces 28-02-2026 (non-leap year).
  Adding 1 month to 31-01-2024 produces 29-02-2024 (leap year).
- Day addition arithmetic (add_days):
  Adds days to date, correctly handling month transitions, leap year Februaries,
  and year-end rollovers (e.g., 28-12-2026 + 7 days = 04-01-2027).
- Day ordinal and difference (days_between):
  Computes absolute elapsed day count from year 1 to calculate precise day
  differences between any two dates without standard library modules.


================================================================================
12. SAMPLE DATA DESCRIPTION
================================================================================
The project files contain realistic, curated baseline sample data:
- members.txt  : 12 member records covering all 4 plans, including active
                 members, expired members, members expiring today, members
                 expiring within 5 days, and members expiring after 7 days.
- payments.txt : 13 payment records spanning multiple months (July, August,
                 September, October 2026, and 2025) to test multi-month revenue.
- checkins.txt : 17 check-in records across multiple months, with several
                 check-ins recorded for member G0002 and others.


================================================================================
13. IMPORTANT ASSUMPTIONS & BOUNDARY RULES
================================================================================
- Active Membership Rule: A membership is considered ACTIVE if and only if
  ExpiryDate >= CurrentDate. A membership expiring today is active throughout
  the day and may check in.
- Expiry Alerts Boundary:
  * Days remaining < 0 : Lapsed / Already Expired.
  * Days remaining == 0: Expires Today (included under alerts).
  * 1 <= Days remaining <= 7: Expiring within 7 days.
  * Days remaining > 7 : Active, not flagged in alerts.
- Revenue Calculation: Revenue is derived solely from payments.txt, ensuring
  historical financial accuracy even after members switch plans.
- Freeze Limit Rule: A membership can be frozen for a maximum total of 15 days
  over its duration. Expired memberships cannot be frozen.
- Trainer Capacity Rule: Each trainer can be assigned a maximum of 10 members.


================================================================================
14. KNOWN LIMITATIONS
================================================================================
- Single-terminal console application: Designed for CLI use without graphical UI.
- No multi-user concurrency lock: Plain-text files are accessed sequentially.
- Pipe character restriction: Member names and IDs cannot contain '|'.
- Single daily date prompt: The session date is captured at startup and remains
  consistent for all transactions in that run.
