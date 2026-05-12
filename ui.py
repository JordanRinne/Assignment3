# Jordan Rinne
# jrinne@uci.edu
# 16935997


import Profile as p
from pathlib import Path
import shlex


def parse(user_input):
    lexer = shlex.shlex(user_input, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    lexer.escape = ""
    return list(lexer)


def run_error(error_type="UNKNOWN EXCEPTION", friendly=True):
    if not friendly:
        print("ERROR")
        return None

    messages = {
        "INVALID COMMAND": "Invalid Command. Use 'C' to create a file,"
        " 'D' to delete a file, 'R' to read a file, 'O' to open a file,"
        " 'E' to edit a profile, or 'P' to print profile information.",
        "INVALID COMMAND (E)": "Invalid Edit Command. Use '-usr' to edit"
        " username, '-pwd' to edit password, '-bio' to edit bio,"
        " '-addpost' to add a post, or '-delpost' to delete a post.",
        "INVALID COMMAND (P)": "Invalid Print Command. Use '-all'"
        " to print all profile information, '-usr' to print username,"
        " '-pwd' to print password, '-bio' to print bio, '-posts'"
        " to print all posts, or '-post <index>' to print a specific post.",
        "INPUT NUMBER ERROR": "Input Number Error. Ensure that you are"
        " providing the correct number of arguments for the command.",
        "PATH ERROR": "Path Error. Ensure that the file path you provided"
        " is valid and that you have the necessary permissions to access it.",
        "FILE ERROR": "File Could Not Be Found. Ensure that the file you are"
        " trying to access exists and is a valid .dsu file.",
        "PROFILE ERROR": "Profile Error. Ensure that the profile you are"
        " trying to access is valid and that you have the necessary"
        " permissions to access it.",
        "INVALID USR/PWD": "Invalid Username or Password. Usernames"
        " and Passwords cannot contain spaces.",
        "EMPTY PARAM": "Empty Parameter. Each profile must have"
        " a non-empty DsuServer, Username, and Password.",
        "INVALID INDEX": "Invalid Index. Ensure that the index you provided"
        " is a valid integer and corresponds to an existing post.",
        "EMPTY FILE": "Empty File. The file you are trying to open is empty"
        " and cannot be loaded as a profile."
    }

    if error_type in messages:
        print(f"{messages[error_type]} Check your input and try again.")
    else:
        print("UNKNOWN EXCEPTION: An unknown error occurred.")


def create_file(user_input, friendly=True):

    if len(user_input) != 3 or user_input[1] != "-n":
        run_error("INPUT NUMBER ERROR", friendly=friendly)
        return None
    directory = user_input[0]
    filename = user_input[2]
    file_path = Path(directory).expanduser() / f"{filename}.dsu"
    if file_path.exists():
        print(f"{file_path} OPENED")
        return file_path, True

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
    except Exception:
        run_error("PATH ERROR", friendly=friendly)
        return None

    if user_input[0][-1] != "/":
        user_input[0] += "/"
    print(f"{user_input[0]}{user_input[2]}.dsu CREATED")
    return file_path, False


def delete_file(user_input, friendly=True):
    if len(user_input) != 1:
        run_error("INPUT NUMBER ERROR", friendly=friendly)
        return None
    name = user_input[0]
    if name[-4:] != ".dsu":
        run_error("FILE ERROR", friendly=friendly)
        return None
    FILE = Path(name).expanduser()
    if not FILE.is_file():
        run_error("FILE ERROR", friendly=friendly)
        return None
    FILE.unlink()
    print(f"{name} DELETED")
    return None


def read_file(user_input, friendly=True):
    if len(user_input) != 1:
        run_error("INPUT NUMBER ERROR", friendly=friendly)
        return None
    name = user_input[0]
    if name[-4:] != ".dsu":
        run_error("FILE ERROR", friendly=friendly)
        return None
    FILE = Path(name).expanduser()
    if not FILE.is_file():
        run_error("FILE ERROR", friendly=friendly)
        return None
    with FILE.open() as f:
        if f.read() == "":
            print("EMPTY")
        else:
            f.seek(0)
            print("\n"+f.read()+"\n")
    return None


def open_file(user_input, friendly=True):
    if len(user_input) != 1:
        run_error("INPUT NUMBER ERROR", friendly=friendly)
        return None
    name = user_input[0]
    if name[-4:] != ".dsu":
        run_error("FILE ERROR", friendly=friendly)
        return None
    FILE = Path(name).expanduser()
    if not FILE.is_file():
        run_error("PATH ERROR", friendly=friendly)
        return None

    with FILE.open() as f:
        try:
            data = f.read()
            if data == "":
                run_error("EMPTY FILE", friendly=friendly)
                return None
            else:
                profile = p.Profile()
                profile.load_profile(str(FILE))
                print(f"{name} OPENED")
                return profile, FILE
        except Exception:
            run_error("PROFILE ERROR", friendly=friendly)
            return None


def create_profile(friendly=True):

    if friendly:
        dsuserver = input("DsuServer: ")
        username = input("Username: ")
        password = input("Password: ")
        bio = input("Bio (optional): ")
    else:
        print("DsuServer:")
        dsuserver = input()
        print("Username:")
        username = input()
        print("Password:")
        password = input()
        print("Bio:")
        bio = input()

    if " " in username or " " in password:
        run_error("INVALID USR/PWD", friendly=friendly)
        return None
    if not dsuserver or not username or not password:
        run_error("EMPTY PARAM", friendly=friendly)
        return None

    profile = p.Profile(dsuserver, username, password)
    profile.bio = bio
    return profile


def check_profile(profile, friendly=True):

    if profile is None:
        run_error("PROFILE ERROR", friendly=friendly)
        return False

    try:
        print(f"DsuServer: {profile.dsuserver}")
        print(f"Username: {profile.username}")
        print(f"Password: {profile.password}")
        print(f"Bio: {profile.bio}")
        return True
    except Exception as e:
        run_error("PROFILE ERROR", friendly=friendly)
        return False


def edit_profile(user_input, profile, path, friendly=True):

    if user_input == ["help"]:
        print("Available edit commands:")
        print("-usr <new_username>: Edit the username of the profile.")
        print("-pwd <new_password>: Edit the password of the profile.")
        print("-bio <new_bio>: Edit the bio of the profile.")
        print(
            "-addpost <post_entry>: Add a new post with the specified"
            " entry to the profile."
        )
        print(
            "-delpost <post_index>: Delete the post at the specified"
            " index from the profile."
        )
        return None

    if profile is None:
        run_error("PROFILE ERROR", friendly=friendly)
        return None

    if len(user_input) < 2:
        run_error("INPUT NUMBER ERROR", friendly=friendly)
        return None

    while len(user_input) > 1:

        if user_input[0] == "-usr":
            if " " in user_input[1]:
                run_error("INVALID USR/PWD", friendly=friendly)
                return None
            profile.username = user_input[1]
            profile.save_profile(path)
            user_input = user_input[2:]

        elif user_input[0] == "-pwd":
            if " " in user_input[1]:
                run_error("INVALID USR/PWD", friendly=friendly)
                return None
            profile.password = user_input[1]
            profile.save_profile(path)
            user_input = user_input[2:]

        elif user_input[0] == "-bio":
            profile.bio = user_input[1]
            profile.save_profile(path)
            user_input = user_input[2:]

        elif user_input[0] == "-addpost":
            post = p.Post(entry=user_input[1])
            profile.add_post(post)
            profile.save_profile(path)
            user_input = user_input[2:]

        elif user_input[0] == "-delpost":
            try:
                index = int(user_input[1])
                if not profile.del_post(index):
                    run_error("INVALID INDEX", friendly=friendly)
                    return None
                profile.save_profile(path)
                user_input = user_input[2:]
            except ValueError:
                run_error("INVALID INDEX", friendly=friendly)
                return None

        else:
            run_error("INVALID COMMAND (E)", friendly=friendly)
            return None
    if len(user_input) == 1:
        run_error("INPUT NUMBER ERROR", friendly=friendly)
        return None
    return None


def print_profile(user_input, profile, friendly=True):

    if user_input == ["help"]:
        print("Available print commands:")
        print(
            "-all: Print all profile information, including username,"
            " password, bio, and all posts."
        )
        print("-usr: Print the username of the profile.")
        print("-pwd: Print the password of the profile.")
        print("-bio: Print the bio of the profile.")
        print("-posts: Print all posts in the profile.")
        print(
            "-post <index>: Print the post at the specified index in"
            " the profile."
        )
        return None

    if profile is None:
        run_error("PROFILE ERROR", friendly=friendly)
        return None

    if len(user_input) < 1:
        run_error("INPUT NUMBER ERROR", friendly=friendly)
        return None

    while len(user_input) > 0:

        if user_input[0] == "-all":
            if not check_profile(profile, friendly=friendly):
                return None
            posts = profile.get_posts()
            for i, post in enumerate(posts):
                print(f"Post {i}: {post.entry} (timestamp: {post.timestamp})")
            user_input = user_input[1:]

        elif user_input[0] == "-usr":
            print(f"Username: {profile.username}")
            user_input = user_input[1:]

        elif user_input[0] == "-pwd":
            print(f"Password: {profile.password}")
            user_input = user_input[1:]

        elif user_input[0] == "-bio":
            print(f"Bio: {profile.bio}")
            user_input = user_input[1:]

        elif user_input[0] == "-posts":
            posts = profile.get_posts()
            for i, post in enumerate(posts):
                print(f"Post {i}: {post.entry} (timestamp: {post.timestamp})")
            user_input = user_input[1:]

        elif (
            user_input[0] == "-post"
            and len(user_input) >= 2
            and user_input[1].isdigit()
        ):
            index = int(user_input[1])
            posts = profile.get_posts()
            post = posts[index] if 0 <= index < len(posts) else None
            if post is None:
                run_error("INVALID INDEX", friendly=friendly)
                return None
            print(f"Post {index}: {post.entry} (timestamp: {post.timestamp})")
            user_input = user_input[2:]

        else:
            run_error("INVALID COMMAND (P)", friendly=friendly)
            return None


def print_help():
    print("Available commands:")
    print(
        "C <directory> -n <filename>: Create a new .dsu file in the"
        " specified directory with the specified filename."
    )
    print("D <filename.dsu>: Delete the specified .dsu file.")
    print(
        "R <filename.dsu>: Read and display the contents of the"
        " specified .dsu file."
    )
    print(
        "O <filename.dsu>: Open the specified .dsu file and load"
        " its contents into a profile."
    )
    print(
        "E <edit commands>: Edit the currently loaded profile using the"
        " specified edit commands. Enter 'E help' for a list of edit commands."
    )
    print(
        "P <print commands>: Print information from the currently loaded"
        " profile using the specified print commands. Enter 'P help' for"
        " a list of print commands."
    )
    print("Q: Quit the program.")
    return None


def admin_mode():
    ans = " "
    profile = None
    file_path = None

    while True:
        try:
            ans = parse(input())
        except Exception:
            run_error(friendly=False)
            continue

        if not ans:
            run_error(friendly=False)
            continue
        if ans[0].lower() == "q":
            break

        if ans[0] == "C":
            result = create_file(ans[1:], friendly=False)
            if result is None:
                continue
            file_path, exists = result
            if not exists:
                profile = create_profile(friendly=False)
                if profile is None:
                    delete_file([str(file_path)], friendly=False)
                    continue
                profile.save_profile(str(file_path))
            if exists:
                try:
                    profile = p.Profile()
                    profile.load_profile(str(file_path))
                except Exception:
                    run_error(friendly=False)

        elif ans[0] == "D":
            delete_file(ans[1:], friendly=False)

        elif ans[0] == "R":
            read_file(ans[1:], friendly=False)

        elif ans[0] == "O":
            result = open_file(ans[1:], friendly=False)
            if result is not None:
                profile, file_path = result

        elif ans[0] == "E":
            try:
                edit_profile(ans[1:], profile, file_path, friendly=False)
            except Exception as e:
                run_error(friendly=False)

        elif ans[0] == "P":
            print_profile(ans[1:], profile, friendly=False)

        elif ans[0] == "help":
            print_help()

        else:
            run_error(friendly=False)
    return None


def main_ui(start):

    ans = parse(start)
    quit = False

    while True:
        if not ans:
            print()
            ans = parse(input(
                "Enter 'new' to create a new profile or"
                " 'load' to load an existing profile (or Q to quit): "
            ))
            continue
        if ans[0] == "new":
            print()
            name = input(
                "What name would you like to give"
                " the profile? (without .dsu extension): "
            )
            print()
            file_path = input(
                "Where would you like to save the"
                " profile? (Enter the directory path): "
            )
            print()
            if not name or not file_path:
                run_error("INPUT NUMBER ERROR")
                continue
            ans = [file_path, "-n", name]
            result = create_file(ans)
            if result is None:
                continue
            print()
            print(
                "Enter the following information"
                f"to create the profile '{name}':"
            )
            file_path, exists = result
            if not exists:
                profile = create_profile()
                if profile is None:
                    delete_file([str(file_path)])
                    continue
                profile.save_profile(str(file_path))
            if exists:
                try:
                    profile = p.Profile()
                    profile.load_profile(str(file_path))
                except Exception:
                    run_error("PROFILE ERROR")
                    continue
            print(f"Profile for {name} created and saved successfully.")
            print()
            print(
                "Now that you have a profile, you can"
                " use any of the following actions:"
            )
            break
        elif ans[0] == "open":
            print()
            name = input(
                "Enter the name of the profile you would like"
                " to open (without .dsu extension): "
            )
            print()
            file_path = input(
                "Enter the directory path where"
                " the profile is located: "
            )
            print()
            ans = [str(Path(file_path).expanduser() / f"{name}.dsu")]
            result = open_file(ans)
            if result is not None:
                profile, file_path = result
                print(f"Profile '{name}' loaded successfully.")
                print()
                print(
                    "Now that you have loaded your profile, you can"
                    " use any of the following actions:"
                )
                break
        elif ans[0].lower() == "q":
            print()
            quit = True
            return None
        else:
            print()
            ans = parse(input(
                "Enter 'new' to create a new profile or 'open' to load"
                " an existing profile: (or Q to quit): "
            ))

    while True and not quit:
        print()
        print("Create another profile (type C)")
        print("Load an existing profile (type O)")
        print("Delete a profile (type D)")
        print("Read a profile (type R)")
        print("Edit a profile (type E)")
        print("Print profile information (type P)")
        print("Quit the program (type Q)")
        print()
        ans = input("What would you like to do? ")
        print()

        if ans.lower() == "q":
            break
        elif ans.lower() == "c":
            name = input(
                "What name would you like to give the profile?"
                " (without .dsu extension): "
            )
            file_path = input(
                "Where would you like to save the profile?"
                " (Enter the directory path): "
            )
            if not name or not file_path:
                run_error("INPUT NUMBER ERROR")
                continue
            ans = [file_path, "-n", name]
            result = create_file(ans)
            if result is None:
                continue

            print(
                "Enter the following information"
                f" to create the profile '{name}': "
            )
            file_path, exists = result
            if not exists:
                profile = create_profile()
                if profile is None:
                    delete_file([str(file_path)])
                    continue
                profile.save_profile(str(file_path))
            if exists:
                try:
                    profile = p.Profile()
                    profile.load_profile(str(file_path))
                except Exception:
                    run_error("PROFILE ERROR")
                    continue
            print(f"Profile for {name} created and saved successfully.")

        elif ans.lower() == "o":
            name = input(
                "Enter the name of the profile you would like to load"
                " (without .dsu extension): "
            )
            file_path = input(
                "Enter the directory path where the profile is located: "
            )
            ans = [str(Path(file_path).expanduser() / f"{name}.dsu")]
            result = open_file(ans)
            if result is not None:
                profile, file_path = result
                print(f"Profile '{name}' loaded successfully.")

        elif ans.lower() == "d":
            name = input(
                "Enter the name of the profile you would like to delete"
                " (without .dsu extension): "
            )
            file_path = input(
                "Enter the directory path where the profile is located: "
            )
            ans = [str(Path(file_path).expanduser() / f"{name}.dsu")]
            delete_file(ans)

        elif ans.lower() == "r":
            name = input(
                "Enter the name of the profile you would like to read"
                " (without .dsu extension): "
            )
            file_path = input(
                "Enter the directory path where the profile is located: "
            )
            ans = [str(Path(file_path).expanduser() / f"{name}.dsu")]
            read_file(ans)

        elif ans.lower() == "e":
            edit_command = input(
                "Enter an edit command (type 'E help'"
                " for a list of possible commands): "
            )
            if not edit_command:
                run_error("INPUT NUMBER ERROR")
                continue
            if edit_command == "E help":
                print()
                edit_profile(["help"], profile, file_path)
                continue
            if edit_command == "-delpost":
                index_str = input(
                    "Enter the index of the post you would like to delete: "
                )
                if index_str.isdigit():
                    edit_profile(["-delpost", index_str], profile, file_path)
                else:
                    run_error("INVALID INDEX")
                continue
            if edit_command not in ["-usr", "-pwd", "-bio", "-addpost"]:
                run_error("INVALID COMMAND (E)")
                continue
            edit_input = input("Enter the new Profile information: ")
            edit_profile([edit_command, edit_input], profile, file_path)

        elif ans.lower() == "p":
            print_command = input(
                "Enter a print command (type 'P help'"
                " for a list of possible commands): "
            )
            if not print_command:
                run_error("INPUT NUMBER ERROR")
                continue
            if print_command == "P help":
                print()
                print_profile(["help"], profile)
                continue
            if print_command in ["-all", "-usr", "-pwd", "-bio", "-posts"]:
                print()
                print_profile([print_command], profile)
            elif print_command.startswith("-post "):
                index_str = print_command[6:].strip()
                if index_str.isdigit():
                    print_profile(["-post", index_str], profile)
                else:
                    run_error("INVALID INDEX")
            else:
                run_error("INVALID COMMAND (P)")
                continue
        else:
            run_error("INVALID COMMAND")
    return None
