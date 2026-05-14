# Jordan Rinne
# jrinne@uci.edu
# 16935997

import ui


def main():

    start = input("Enter an input: ")

    if start == "admin":
        ui.admin_mode()
    else:
        ui.main_ui(start)
        
    return None


if __name__ == "__main__":
    main()
    