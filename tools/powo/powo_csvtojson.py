from powo_csvtojson_functions import *

script_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = os.path.join(script_dir, "../../input/powo")
raw = os.path.join(folder_path, "raw")
currated = os.path.join(folder_path, "currated")


if __name__ == "__main__":
    wcvpJson(raw, currated)
