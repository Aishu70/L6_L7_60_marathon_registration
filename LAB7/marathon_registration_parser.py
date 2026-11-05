def format_bib_name(name):
    """
    Upper-cases a runner's name and cuts it to 12 characters.
    Returns an empty string for invalid input.
    """

    if not isinstance(name, str):
        return ""

    return name.strip().upper()[:12]


def parse_finish_time(text):
    """
    Converts a finish time written as H:MM:SS into seconds.
    Returns 0 for invalid input.
    """

    if not isinstance(text, str):
        return 0

    parts = text.split(':')

    if len(parts) != 3:
        return 0

    if not all(part.isdigit() for part in parts):
        return 0

    hours, minutes, seconds = map(int, parts)

    if minutes >= 60 or seconds >= 60:
        return 0

    return hours * 3600 + minutes * 60 + seconds


def average_split(text):
    """
    Averages split times given in minutes.
    Returns 0 for invalid input.
    """

    if not isinstance(text, str):
        return 0

    try:
        splits = [int(s) for s in text.split()]
    except ValueError:
        return 0

    if not splits:
        return 0

    if any(split < 0 for split in splits):
        return 0

    return sum(splits) / len(splits)


def main():
    print("==== Running format_bib_name ====")
    value = input("Enter the name to print on the bib: ")
    print("Bib name:", format_bib_name(value))

    print("\n==== Running parse_finish_time ====")
    value = input("Enter a finish time as H:MM:SS (e.g. 3:45:10): ")
    print("Finish time in seconds:", parse_finish_time(value))

    print("\n==== Running average_split ====")
    value = input(
        "Enter your 5 km split times in minutes separated by spaces "
        "(e.g. 25 26 24): "
    )
    print("Average split (minutes):", average_split(value))


if __name__ == "__main__":
    main()