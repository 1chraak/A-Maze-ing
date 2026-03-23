import sys
from typing import Any
from mazegen.mazegen import MazeGenerator, Config
from export.create_output import hex_file
from utils.pathfinder import path
from display.display import menu_loop


def key_check(key: str) -> bool:
    '''To check if the key is in the list of valid keys'''

    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    if key.strip().upper() not in keys:
        return False
    return True


def parse_value(key: str, value: str) -> Any:
    '''Parses the configuration file'''

    if key == "WIDTH" or key == "HEIGHT":
        num = int(value)
        if key == "WIDTH" and num < 10:
            raise ValueError
        if key == "HEIGHT" and num < 8:
            raise ValueError
        return num

    if key == "ENTRY" or key == "EXIT":
        if "," not in value:
            raise ZeroDivisionError("Value for (ENTRY/EXIT) "
                                    "must br in the form 'X,Y'")
        if len(value.split(",")) > 2:
            raise ZeroDivisionError("Too many parameters, or too many ','. "
                                    "Value for (ENTRY/EXIT) must br in the "
                                    "form 'X,Y'")
        x = int(value.split(",")[0].strip())
        y = int(value.split(",")[1].strip())
        if x < 0 or y < 0:
            raise ZeroDivisionError("Cannot have negative coordinates")
        return (x, y)

    if key == "OUTPUT_FILE":
        if ".txt" not in value or " " in value or len(value) < 5:
            raise ZeroDivisionError("Invalid output file name, follow this "
                                    "example: 'file_name.txt'. (No space in "
                                    "name, must be .txt)")
        return value

    if key == "PERFECT":
        if value.upper() != "TRUE" and value.upper() != "FALSE":
            raise ZeroDivisionError("Invalid value, must be (true/false), "
                                    "lower or upper case all the same")
        if value.upper() == "TRUE":
            return True
        return False


def read_config(file: str) -> Config:
    '''The function for "config.txt" format checking.
        And configuration object creation'''

    all_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    key_count = []
    config: dict[str, Any] = {}
    try:
        with open(file, "r") as f:
            lines = f.read().split("\n")
            for line in lines:
                if not line or line[0] == "#":
                    continue
                if "=" not in line:
                    raise ZeroDivisionError("Line does not contain '=' "
                                            "for assigning")
                if len(line.split("=")) != 2:
                    raise ZeroDivisionError("Please stick to the format: "
                                            "KEY=VALUE")
                if not key_check(line.split("=")[0]):
                    raise ZeroDivisionError(f"{line} must have a key from "
                                            "[WIDTH, HEIGHT, ENTRY, EXIT, "
                                            "OUTPUT_FILE, PERFECT], upper "
                                            "or lower case")
                key = line.split("=")[0].strip().upper()
                if key in key_count:
                    raise ZeroDivisionError(f"Cannot have the same key more "
                                            f"than once: {key}")
                else:
                    key_count.append(key)
            if len(key_count) != len(all_keys):
                raise ZeroDivisionError("All keys [WIDTH, HEIGHT, ENTRY, EXIT"
                                        ", OUTPUT_FILE, PERFECT] must be "
                                        "present in the config file, and have "
                                        "valid input.")
            config = dict.fromkeys(key_count)
            for line in lines:
                if not line or line[0] == "#":
                    continue
                key = line.split("=")[0].strip().upper()
                value = line.split("=")[1].strip()
                config[key] = parse_value(key, value)

            if (config["ENTRY"][0] >= config["WIDTH"]
                    or config["ENTRY"][1] >= config["HEIGHT"]):
                raise PermissionError("Entry coordinates out of bound")

            if (config["EXIT"][0] >= config["WIDTH"]
                    or config["EXIT"][1] >= config["HEIGHT"]):
                raise PermissionError("Exit coordinates out of bound")

            if (config["ENTRY"][0] == config["EXIT"][0]
                    and config["ENTRY"][1] == config["EXIT"][1]):
                raise PermissionError("ENTRY and EXIT must NOT "
                                      "have the same coordinates")

            return Config(width=config["WIDTH"],
                          height=config["HEIGHT"],
                          entry=config["ENTRY"],
                          exit=config["EXIT"],
                          output_file=config["OUTPUT_FILE"],
                          perfect=config["PERFECT"])

    except ValueError:
        print("Make sure all numbers are valid and Non negative, "
              "(WIDTH > 10, HEIGHT > 8) for 42 logo\n")
        sys.exit()
    except FileNotFoundError:
        print(f"File {file} not found\n")
        sys.exit()
    except ZeroDivisionError as e:
        print(f"Parsing ERROR: {e}\n")
        sys.exit()
    except PermissionError as e:
        print(f"{e}\n")
        sys.exit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You must use: python3 a_maze_ing.py config.txt")
        sys.exit()

    while True:
        config = read_config(sys.argv[1])
        maze = MazeGenerator(config)
        maze.generate()
        solution = path(maze)

        hex_file(maze, solution, config.output_file)
    
        action = menu_loop(maze)
        if action == "regenerate":
            continue
        if action == "quit":
            break
