# Name: Saadhana Durga S
# Register Number: 7376252IT316
# Project: P25 Gym Membership Manager

# File constants
MEMBERS_FILE = "members.txt"
PAYMENTS_FILE = "payments.txt"
CHECKINS_FILE = "checkins.txt"

# Global current date variables (set once at startup)
TODAY = ""
TODAY_NUM = 0

# Membership plan configuration
PLAN_NAMES = ["Monthly", "Quarterly", "Half-yearly", "Annual"]
PLAN_PRICES = [1200, 3300, 6000, 10800]
PLAN_MONTHS = [1, 3, 6, 12]

# Bonus feature constants
MAX_FREEZE_DAYS = 15
MAX_TRAINER_CAPACITY = 10
TRAINER_ROSTER = {
    "T01": "Coach Vikram",
    "T02": "Coach Priya",
    "T03": "Coach Marcus"
}


# ==============================================================================
# 1. DATE VALIDATION AND DATE ARITHMETIC (NO EXTERNAL IMPORTS)
# ==============================================================================

def is_leap_year(year):
    """
    Checks if a year is a leap year using Gregorian calendar rules:
    Divisible by 400, or divisible by 4 and not divisible by 100.
    """
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)


def days_in_month(month, year):
    """
    Returns the maximum number of days in a given month and year.
    """
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    return 0


def is_valid_date(date_text):
    """
    Validates date strictly in DD-MM-YYYY format with 2-digit day,
    2-digit month, 4-digit year, and realistic calendar boundaries.
    """
    if not date_text or not isinstance(date_text, str):
        return False
    parts = date_text.strip().split("-")
    if len(parts) != 3:
        return False
    if len(parts[0]) != 2 or len(parts[1]) != 2 or len(parts[2]) != 4:
        return False
    if not (parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit()):
        return False
    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
    if year < 1 or month < 1 or month > 12:
        return False
    return 1 <= day <= days_in_month(month, year)


def read_date(prompt="Enter date (DD-MM-YYYY): "):
    """
    Repeatedly prompts the user until a valid DD-MM-YYYY date is entered.
    """
    while True:
        date_text = input(prompt).strip()
        if is_valid_date(date_text):
            return date_text
        print("Invalid date. Please use DD-MM-YYYY format with realistic values.")


def date_parts(date_text):
    """
    Splits DD-MM-YYYY into integer day, month, and year.
    """
    parts = date_text.strip().split("-")
    return int(parts[0]), int(parts[1]), int(parts[2])


def to_number(date_text):
    """
    Converts DD-MM-YYYY to YYYYMMDD integer for fast chronological comparison.
    """
    day, month, year = date_parts(date_text)
    return year * 10000 + month * 100 + day


def date_ordinal(date_text):
    """
    Calculates absolute day count from year 1 to the given date for day differences.
    """
    day, month, year = date_parts(date_text)
    prev_year = year - 1
    total = (
        prev_year * 365
        + prev_year // 4
        - prev_year // 100
        + prev_year // 400
    )
    for m in range(1, month):
        total += days_in_month(m, year)
    return total + day


def days_between(start_date, end_date):
    """
    Returns (end_date - start_date) in days.
    Positive if end_date is after start_date, negative if before, 0 if same day.
    """
    return date_ordinal(end_date) - date_ordinal(start_date)


def add_days(date_text, days_to_add):
    """
    Adds a specified number of days to a DD-MM-YYYY date, correctly
    crossing month and year boundaries and respecting leap years.
    """
    day, month, year = date_parts(date_text)
    day += days_to_add
    while True:
        max_d = days_in_month(month, year)
        if day <= max_d:
            break
        day -= max_d
        month += 1
        if month > 12:
            month = 1
            year += 1
    return f"{day:02d}-{month:02d}-{year:04d}"


def add_months(date_text, months_to_add):
    """
    Adds a given number of months to a DD-MM-YYYY date. Clamps to month end
    when day exceeds target month length (e.g. 31-01-2026 + 1m = 28-02-2026).
    """
    day, month, year = date_parts(date_text)
    total_months = (month - 1) + months_to_add
    new_month = (total_months % 12) + 1
    new_year = year + (total_months // 12)
    max_day = days_in_month(new_month, new_year)
    new_day = min(day, max_day)
    return f"{new_day:02d}-{new_month:02d}-{new_year:04d}"


# ==============================================================================
# 2. FILE HANDLING AND RECORD PARSING HELPERS
# ==============================================================================

def read_records(filename):
    """
    Safely reads lines from a text file. Returns empty list if file not found.
    """
    try:
        with open(filename, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def append_record(filename, record):
    """
    Appends a single line to a text file. Creates the file if not present.
    """
    with open(filename, "a") as file:
        file.write(record + "\n")


def write_records(filename, records):
    """
    Overwrites a text file with a list of lines.
    """
    with open(filename, "w") as file:
        file.writelines(records)


def parse_member_fields(line):
    """
    Parses a member line. Handles standard 6 fields as well as optional
    bonus fields (TrainerID, FreezeDays), ensuring uniform 8-element list.
    """
    line = line.strip()
    if not line:
        return None
    parts = line.split("|")
    if len(parts) < 6:
        return None
    while len(parts) < 8:
        if len(parts) == 6:
            parts.append("Unassigned")
        elif len(parts) == 7:
            parts.append("0")
    return parts


def generate_member_id():
    """
    Scans members.txt and generates the next available unique Member ID (e.g., G0013).
    """
    highest = 0
    for line in read_records(MEMBERS_FILE):
        parts = parse_member_fields(line)
        if parts and parts[0].startswith("G"):
            num_str = parts[0][1:]
            if num_str.isdigit():
                num = int(num_str)
                if num > highest:
                    highest = num
    return f"G{highest + 1:04d}"


def find_member(member_id):
    """
    Finds a member by Member ID in members.txt.
    Returns parsed details list or None if not found.
    """
    for line in read_records(MEMBERS_FILE):
        parts = parse_member_fields(line)
        if parts and parts[0] == member_id:
            return parts
    return None


def format_member_record(details):
    """
    Formats a member record for file saving. Retains standard 6 fields
    unless bonus features (trainer or freeze) have active assignments.
    """
    if len(details) > 6:
        trainer = details[6]
        freeze = details[7] if len(details) > 7 else "0"
        if trainer != "Unassigned" or (freeze.isdigit() and int(freeze) > 0):
            return "|".join(details)
    return "|".join(details[:6])


def save_member_details(updated_details):
    """
    Updates an existing member record in members.txt.
    """
    records = read_records(MEMBERS_FILE)
    updated = False
    for i in range(len(records)):
        parts = parse_member_fields(records[i])
        if parts and parts[0] == updated_details[0]:
            records[i] = format_member_record(updated_details) + "\n"
            updated = True
            break
    if updated:
        write_records(MEMBERS_FILE, records)
        return True
    return False


# ==============================================================================
# 3. USER INPUT HELPERS (SAFE READERS & VALIDATORS)
# ==============================================================================

def read_int(prompt, low, high):
    """
    Reads an integer within the specified inclusive range [low, high].
    Re-prompts with a clear message on invalid, empty, or out-of-range input.
    """
    while True:
        text = input(prompt).strip()
        if text.isdigit():
            val = int(text)
            if low <= val <= high:
                return val
        print(f"Invalid input. Please enter a whole number between {low} and {high}.")


def read_member_id(prompt="Enter Member ID (e.g., G0001): "):
    """
    Reads and validates a Member ID string. Re-prompts on empty input or pipe.
    """
    while True:
        mid = input(prompt).strip().upper()
        if not mid:
            print("Member ID cannot be empty. Please enter a valid ID.")
        elif "|" in mid:
            print("The character '|' is reserved and cannot be used in Member IDs.")
        else:
            return mid


def get_member_name():
    """
    Validates that member name is non-empty and does not contain '|'.
    """
    while True:
        name = input("Enter member name: ").strip()
        if not name:
            print("Name cannot be empty. Please enter a valid name.")
        elif "|" in name:
            print("The character '|' is reserved and cannot be used in names.")
        else:
            return name


def get_phone_number():
    """
    Validates that phone number is exactly 10 numeric digits.
    """
    while True:
        phone = input("Enter phone number (10 digits): ").strip()
        if len(phone) == 10 and phone.isdigit():
            return phone
        print("Invalid phone number. Must be exactly 10 digits (e.g., 9876543210).")


def show_plans():
    """
    Displays the four available membership plans, durations, and prices.
    """
    print("\n--- AVAILABLE MEMBERSHIP PLANS ---")
    for index in range(len(PLAN_NAMES)):
        print(
            f"  {index + 1}. {PLAN_NAMES[index]:<12} - "
            f"{PLAN_MONTHS[index]:>2} month(s) - "
            f"Rs. {PLAN_PRICES[index]:,}"
        )


def choose_plan():
    """
    Allows user to select a plan by number (1-4) or plan name (case-insensitive).
    """
    show_plans()
    while True:
        choice = input("Select plan (1-4 or plan name): ").strip()
        if choice in ["1", "2", "3", "4"]:
            return int(choice) - 1
        choice_clean = choice.lower().replace(" ", "-")
        for index in range(len(PLAN_NAMES)):
            plan_clean = PLAN_NAMES[index].lower()
            if choice_clean == plan_clean or choice.lower() == plan_clean:
                return index
        print("Invalid choice. Please enter 1, 2, 3, 4 or plan name (e.g., Monthly).")


def read_month_year(prompt_prefix=""):
    """
    Reads and validates month (1-12) and 4-digit positive year.
    """
    month = read_int(f"{prompt_prefix}Enter month (1-12): ", 1, 12)
    year = read_int(f"{prompt_prefix}Enter year (YYYY): ", 1, 9999)
    return month, year


# ==============================================================================
# 4. CORE APPLICATION FEATURES (OPTIONS 1 TO 7)
# ==============================================================================

def register_member():
    """
    Option 1: Register a new member with auto-generated ID.
    Calculates expiry date, appends to members.txt and payments.txt.
    """
    print("\n--- REGISTER NEW MEMBER ---")
    name = get_member_name()
    phone = get_phone_number()
    plan_index = choose_plan()

    join_date = TODAY
    plan_name = PLAN_NAMES[plan_index]
    price = PLAN_PRICES[plan_index]
    expiry_date = add_months(join_date, PLAN_MONTHS[plan_index])
    member_id = generate_member_id()

    record = format_member_record([member_id, name, phone, plan_name, join_date, expiry_date, "Unassigned", "0"])
    append_record(MEMBERS_FILE, record)
    append_record(PAYMENTS_FILE, f"{member_id}|{TODAY}|{plan_name}|{price}")

    print("\n[SUCCESS] Member registered successfully!")
    print(f"  Member ID    : {member_id}")
    print(f"  Name         : {name}")
    print(f"  Phone        : {phone}")
    print(f"  Plan         : {plan_name}")
    print(f"  Joining Date : {join_date}")
    print(f"  Expiry Date  : {expiry_date}")
    print(f"  Amount Paid  : Rs. {price:,}")


def view_members():
    """
    Option 2: Display registered members in an aligned terminal table.
    """
    print("\n--- REGISTERED MEMBERS ---")
    members = []
    for line in read_records(MEMBERS_FILE):
        parts = parse_member_fields(line)
        if parts and parts[0].startswith("G") and is_valid_date(parts[5]):
            members.append(parts)

    if not members:
        print("No registered members found.")
        return

    header = f"{'ID':<8} {'Name':<22} {'Phone':<14} {'Plan':<14} {'Join Date':<12} {'Expiry Date':<12}"
    divider = "-" * len(header)
    print(divider)
    print(header)
    print(divider)
    for m in members:
        print(f"{m[0]:<8} {m[1]:<22} {m[2]:<14} {m[3]:<14} {m[4]:<12} {m[5]:<12}")
    print(divider)
    print(f"Total Members: {len(members)}")


def display_member_card(details):
    """
    Helper function to display current member details and status.
    """
    is_active = to_number(details[5]) >= TODAY_NUM
    status_str = "Active" if is_active else "Expired"
    print("\n--- Current Member Details ---")
    print(f"  Member ID    : {details[0]}")
    print(f"  Name         : {details[1]}")
    print(f"  Phone        : {details[2]}")
    print(f"  Current Plan : {details[3]}")
    print(f"  Joining Date : {details[4]}")
    print(f"  Expiry Date  : {details[5]}")
    print(f"  Trainer      : {details[6]}")
    print(f"  Status       : {status_str}")
    return is_active


def renew_membership():
    """
    Option 3: Renew membership. Extends from current expiry date if active,
    or from TODAY if expired. Updates members.txt and records payment.
    """
    print("\n--- RENEW MEMBERSHIP ---")
    member_id = read_member_id()
    details = find_member(member_id)
    if details is None:
        print("Member ID not found.")
        return
    if not is_valid_date(details[5]):
        print("Error: Member record contains an invalid expiry date.")
        return

    is_active = display_member_card(details)
    print("\nSelect the new plan for renewal:")
    plan_index = choose_plan()
    new_plan = PLAN_NAMES[plan_index]
    price = PLAN_PRICES[plan_index]

    renewal_start = details[5] if is_active else TODAY
    new_expiry = add_months(renewal_start, PLAN_MONTHS[plan_index])
    details[3] = new_plan
    details[5] = new_expiry

    if save_member_details(details):
        append_record(PAYMENTS_FILE, f"{member_id}|{TODAY}|{new_plan}|{price}")
        print("\n[SUCCESS] Membership renewed successfully!")
        print(f"  Member ID      : {member_id}")
        print(f"  Name           : {details[1]}")
        print(f"  New Plan       : {new_plan}")
        print(f"  Renewal Basis  : Calculated from {renewal_start}")
        print(f"  New Expiry Date: {new_expiry}")
        print(f"  Amount Paid    : Rs. {price:,}")
    else:
        print("Error: Could not update member record in file.")


def print_alert_section(title, member_list, is_expired):
    """
    Helper function to render an aligned table of expiry alerts.
    """
    print(f"=== {title} ===")
    print(f"{'ID':<8} {'Name':<22} {'Plan':<14} {'Expiry Date':<14} {'Status'}")
    print("-" * 75)
    for details, days in member_list:
        if is_expired:
            status = f"Expired {days} day(s) ago"
        elif days == 0:
            status = "Expires TODAY"
        else:
            status = f"Expires in {days} day(s)"
        print(f"{details[0]:<8} {details[1]:<22} {details[3]:<14} {details[5]:<14} {status}")
    print("-" * 75)
    print()


def show_expiry_alerts():
    """
    Option 4: Lists members already expired and members expiring within next 7 days.
    """
    print("\n--- MEMBERSHIP EXPIRY ALERTS ---")
    print(f"Current Date: {TODAY}\n")
    expired_members = []
    expiring_soon_members = []

    for line in read_records(MEMBERS_FILE):
        parts = parse_member_fields(line)
        if not parts or not is_valid_date(parts[5]):
            continue
        days_left = days_between(TODAY, parts[5])
        if days_left < 0:
            expired_members.append((parts, abs(days_left)))
        elif days_left <= 7:
            expiring_soon_members.append((parts, days_left))

    if not expired_members and not expiring_soon_members:
        print("No expired or soon-to-expire memberships found.")
        return
    if expired_members:
        print_alert_section("ALREADY EXPIRED MEMBERSHIPS", expired_members, True)
    if expiring_soon_members:
        print_alert_section("EXPIRING TODAY / WITHIN NEXT 7 DAYS", expiring_soon_members, False)


def check_in():
    """
    Option 5: Records daily check-in, refusing expired members.
    """
    print("\n--- DAILY CHECK-IN ---")
    member_id = read_member_id()
    details = find_member(member_id)
    if details is None:
        print("Member ID not found.")
        return
    if not is_valid_date(details[5]):
        print("Error: Member record contains an invalid expiry date.")
        return
    if days_between(TODAY, details[5]) < 0:
        print(f"Check-in refused: Membership for {details[1]} ({member_id}) expired on {details[5]}.")
        return

    append_record(CHECKINS_FILE, f"{member_id}|{TODAY}")
    print(f"[SUCCESS] Check-in recorded for {details[1]} ({member_id}) on {TODAY}.")


def monthly_checkin_count():
    """
    Option 6: Counts check-ins for a member in a given month and year.
    """
    print("\n--- MONTHLY CHECK-IN COUNT ---")
    member_id = read_member_id()
    member = find_member(member_id)
    if member is None:
        print("Member ID not found.")
        return

    month, year = read_month_year()
    count = 0
    for line in read_records(CHECKINS_FILE):
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) == 2 and parts[0] == member_id and is_valid_date(parts[1]):
            d, m, y = date_parts(parts[1])
            if m == month and y == year:
                count += 1
    print(f"\nTotal check-ins for {member[1]} ({member_id}) in {month:02d}-{year}: {count}")


def calculate_monthly_revenue(month, year):
    """
    Calculates total revenue and payment transaction count for a month/year.
    """
    revenue = 0
    count = 0
    for line in read_records(PAYMENTS_FILE):
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) == 4 and is_valid_date(parts[1]):
            d, p_month, p_year = date_parts(parts[1])
            if p_month == month and p_year == year:
                if parts[3].isdigit():
                    revenue += int(parts[3])
                    count += 1
    return count, revenue


def calculate_active_members():
    """
    Counts active members across all four membership plans as of TODAY.
    """
    plan_counts = [0, 0, 0, 0]
    total_active = 0
    for line in read_records(MEMBERS_FILE):
        parts = parse_member_fields(line)
        if parts and is_valid_date(parts[5]):
            if days_between(TODAY, parts[5]) >= 0:
                for idx in range(len(PLAN_NAMES)):
                    if parts[3].strip().lower() == PLAN_NAMES[idx].lower():
                        plan_counts[idx] += 1
                        total_active += 1
                        break
    return plan_counts, total_active


def monthly_report():
    """
    Option 7: Monthly revenue report and active member counts by plan.
    """
    print("\n--- MONTHLY REVENUE & ACTIVE MEMBER REPORT ---")
    month, year = read_month_year()
    pmt_count, revenue = calculate_monthly_revenue(month, year)

    print(f"\n{'=' * 46}")
    print(f" REVENUE REPORT FOR {month:02d}-{year}")
    print(f"{'=' * 46}")
    print(f"  Total Payments Received : {pmt_count}")
    print(f"  Total Monthly Revenue   : Rs. {revenue:,}")
    print(f"{'=' * 46}")

    plan_counts, total_active = calculate_active_members()
    print(f"\n{'=' * 46}")
    print(f" CURRENT ACTIVE MEMBERS BY PLAN (as of {TODAY})")
    print(f"{'=' * 46}")
    for idx in range(len(PLAN_NAMES)):
        print(f"  {PLAN_NAMES[idx]:<14} : {plan_counts[idx]} member(s)")
    print(f"{'-' * 46}")
    print(f"  Total Active   : {total_active} member(s)")
    print(f"{'=' * 46}")


# ==============================================================================
# 5. BONUS FEATURES (OPTIONS 9 AND 10)
# ==============================================================================

def freeze_membership():
    """
    Bonus A (Option 9): Freezes an active membership for up to 15 days,
    extending the expiry date accordingly. Prevents freeze abuse.
    """
    print("\n--- MEMBERSHIP FREEZE (BONUS FEATURE) ---")
    member_id = read_member_id()
    details = find_member(member_id)
    if details is None:
        print("Member ID not found.")
        return

    if days_between(TODAY, details[5]) < 0:
        print(f"Cannot freeze membership: Membership for {details[1]} ({member_id}) expired on {details[5]}.")
        return

    used_freeze = int(details[7]) if details[7].isdigit() else 0
    remaining_freeze = MAX_FREEZE_DAYS - used_freeze
    if remaining_freeze <= 0:
        print(f"Freeze refused: Member {details[1]} has already utilized the maximum {MAX_FREEZE_DAYS} freeze days.")
        return

    print(f"Member {details[1]} has used {used_freeze}/{MAX_FREEZE_DAYS} freeze days ({remaining_freeze} day(s) remaining).")
    duration = read_int(f"Enter freeze duration in days (1-{remaining_freeze}): ", 1, remaining_freeze)

    old_expiry = details[5]
    new_expiry = add_days(old_expiry, duration)
    details[5] = new_expiry
    details[7] = str(used_freeze + duration)

    if save_member_details(details):
        print("\n[SUCCESS] Membership frozen successfully!")
        print(f"  Member ID        : {member_id}")
        print(f"  Name             : {details[1]}")
        print(f"  Freeze Duration  : {duration} day(s)")
        print(f"  Previous Expiry  : {old_expiry}")
        print(f"  Extended Expiry  : {new_expiry}")
        print(f"  Total Used Freeze: {details[7]}/{MAX_FREEZE_DAYS} day(s)")
    else:
        print("Error: Could not update member record in file.")


def get_trainer_member_count(trainer_id):
    """
    Returns the count of active gym members assigned to a specific trainer.
    """
    count = 0
    for line in read_records(MEMBERS_FILE):
        parts = parse_member_fields(line)
        if parts and parts[6] == trainer_id:
            count += 1
    return count


def show_trainer_roster():
    """
    Displays the current personal trainers, assigned counts, and capacity.
    """
    print("\n--- PERSONAL TRAINER ROSTER & CAPACITY ---")
    print(f"{'Trainer ID':<12} {'Trainer Name':<20} {'Assigned Members':<18} {'Capacity'}")
    print("-" * 65)
    for tid, tname in sorted(TRAINER_ROSTER.items()):
        cnt = get_trainer_member_count(tid)
        print(f"{tid:<12} {tname:<20} {cnt:>2} / {MAX_TRAINER_CAPACITY:<13} {'Available' if cnt < MAX_TRAINER_CAPACITY else 'FULL'}")
    print("-" * 65)


def assign_trainer():
    """
    Bonus B (Option 10): Assigns or reassigns a member to a personal trainer.
    Strictly enforces the limit of 10 members per trainer.
    """
    print("\n--- ASSIGN PERSONAL TRAINER (BONUS FEATURE) ---")
    member_id = read_member_id()
    details = find_member(member_id)
    if details is None:
        print("Member ID not found.")
        return

    show_trainer_roster()
    current_trainer = details[6]
    print(f"\nMember: {details[1]} ({member_id}) | Current Trainer: {current_trainer}")

    while True:
        tid = input("Enter Trainer ID to assign (e.g., T01, T02, T03) or 'CANCEL': ").strip().upper()
        if tid == "CANCEL":
            print("Trainer assignment cancelled.")
            return
        if tid in TRAINER_ROSTER:
            break
        print("Invalid Trainer ID. Please choose from available trainers (T01, T02, T03).")

    if current_trainer == tid:
        print(f"Member {details[1]} is already assigned to {TRAINER_ROSTER[tid]} ({tid}).")
        return

    assigned_count = get_trainer_member_count(tid)
    if assigned_count >= MAX_TRAINER_CAPACITY:
        print(f"Error: {TRAINER_ROSTER[tid]} ({tid}) is at maximum capacity (10/{MAX_TRAINER_CAPACITY} members). Assignment rejected.")
        return

    details[6] = tid
    if save_member_details(details):
        print(f"\n[SUCCESS] Member {details[1]} ({member_id}) successfully assigned to {TRAINER_ROSTER[tid]} ({tid})!")
        print(f"Trainer {TRAINER_ROSTER[tid]} now has {assigned_count + 1}/{MAX_TRAINER_CAPACITY} members assigned.")
    else:
        print("Error: Could not update member record in file.")


# ==============================================================================
# 6. MAIN MENU AND APPLICATION LIFECYCLE
# ==============================================================================

def show_menu():
    """
    Displays the application terminal menu with all options.
    """
    print("\n========== GYM MEMBERSHIP MANAGER ==========")
    print("1. Register member")
    print("2. View all members")
    print("3. Renew membership")
    print("4. Show expiry alerts")
    print("5. Record daily check-in")
    print("6. Count monthly check-ins")
    print("7. Monthly revenue and active member report")
    print("8. Exit")
    print("--- Optional Bonus Features ---")
    print("9. Freeze membership (Bonus A)")
    print("10. Assign personal trainer (Bonus B)")
    print("============================================")


def main():
    """
    Application entry point. Prompts today's date once at startup,
    then enters the interactive menu loop.
    """
    global TODAY, TODAY_NUM
    print("==================================================")
    print("  WELCOME TO P25 GYM MEMBERSHIP MANAGER")
    print("==================================================")
    TODAY = read_date("Enter today's date (DD-MM-YYYY): ")
    TODAY_NUM = to_number(TODAY)
    print(f"Session initialized with current date: {TODAY}")

    while True:
        show_menu()
        choice = input("Enter your choice (1-10): ").strip()
        if choice == "1":
            register_member()
        elif choice == "2":
            view_members()
        elif choice == "3":
            renew_membership()
        elif choice == "4":
            show_expiry_alerts()
        elif choice == "5":
            check_in()
        elif choice == "6":
            monthly_checkin_count()
        elif choice == "7":
            monthly_report()
        elif choice == "8":
            print("\nThank you for using Gym Membership Manager. Goodbye!")
            break
        elif choice == "9":
            freeze_membership()
        elif choice == "10":
            assign_trainer()
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
