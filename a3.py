# Jordan Rinne
# jrinne@uci.edu
# 16935997

import ui


def main():

    start = input("Enter 'new' to create a new profile, or 'load' to load an existing one: ")

    if start == "admin":
        ui.admin_mode()
    else:
        ui.main_ui(start)
        print("Exiting program. Goodbye!")
        print()

    return None


if __name__ == "__main__":
    main()