"""Convert a Twiddler (V5?) config in CSV format to JSON format for use with the Tutor app.

See https://forum.tekgear.com/t/question-about-tutor-and-custom-cfg/796/9?u=brandonwillard
"""
import json
import pandas as pd


cfg_csv = pd.read_csv("twiddler_cfg.csv")
cfg_csv.columns = ["chord", "key"]
cfg_csv.chord = cfg_csv.chord.str.strip()
cfg_csv[["m", "chord"]] = cfg_csv.chord.str.split(" ", expand=True)

cfg_dict = cfg_csv.to_dict(orient="records")
cfg_dict = {"chords": cfg_dict}

with open("twiddler_cfg.json", "w") as f:
    json.dump(cfg_dict, f)
