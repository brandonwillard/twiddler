"""Add V5 thumb modifier keys to a Twiddler V6 config in CSV format."""

import warnings
import pathlib
import csv
import pandas as pd


config_csv_file = "tabspace_twiddler_V6.csv"

cfg_csv = pd.read_csv(
    config_csv_file,
    header=0,
    names=["Thumbs", "Fingers", "Actions"],
    dtype={"Thumbs": str, "Fingers": str, "Actions": str},
    keep_default_na=False,
)

shift_thumb_key = "4"
shift_label = "L-Shift"
ctrl_thumb_key = "3"
ctrl_label = "L-Ctrl"
alt_thumb_key = "2"
alt_label = "L-Alt"


def add_modifier(action: str, modifier_label: str) -> str:
    return f"<{modifier_label}>" + action + f"</{modifier_label}>"


def should_add_modifier(entry: dict, modifier_thumb_key) -> bool:
    # We probably don't want to add modifiers to "[SYS]" entries.
    if not entry["Actions"].startswith("[KB]"):
        return False

    # This would be redundant
    if modifier_thumb_key in entry["Thumbs"]:
        return False

    return True


chords_to_actions = {}
new_cfg = []


def check_and_add_entry(entry, warn=True):

    chord_key = (entry["Thumbs"], entry["Fingers"])

    existing_action = chords_to_actions.get(chord_key)
    if existing_action is not None and entry["Actions"] != existing_action and warn:
        warnings.warn(
            f"Chord {entry} is already mapped to {existing_action}; skipping"
        )
        return

    chords_to_actions[chord_key] = entry["Actions"]
    new_cfg.append(entry)


for entry in cfg_csv.to_dict(orient="records"):
    new_cfg.append(entry)

    sorted_thumbs = "".join(sorted(entry["Thumbs"]))
    if sorted_thumbs != entry["Thumbs"]:
        warnings.warn(f"Thumb entries are not sorted in {entry}")
        entry["Thumbs"] = sorted_thumbs

    check_and_add_entry(entry)

    add_shift = should_add_modifier(entry, shift_thumb_key)
    add_ctrl = should_add_modifier(entry, ctrl_thumb_key)
    add_alt = should_add_modifier(entry, alt_thumb_key)

    entry_action = entry["Actions"].split("[KB]")[-1]

    if add_shift:
        new_entry = {
            "Thumbs": "".join(sorted(entry["Thumbs"] + shift_thumb_key)),
            "Fingers": entry["Fingers"],
            "Actions": "[KB]" + add_modifier(entry_action, shift_label),
        }
        check_and_add_entry(new_entry)

    if add_ctrl:
        new_entry = {
            "Thumbs": "".join(sorted(entry["Thumbs"] + ctrl_thumb_key)),
            "Fingers": entry["Fingers"],
            "Actions": "[KB]" + add_modifier(entry_action, ctrl_label),
        }
        check_and_add_entry(new_entry)

    if add_alt:
        new_entry = {
            "Thumbs": "".join(sorted(entry["Thumbs"] + alt_thumb_key)),
            "Fingers": entry["Fingers"],
            "Actions": "[KB]" + add_modifier(entry_action, alt_label),
        }
        check_and_add_entry(new_entry)

    if add_shift or add_ctrl:
        new_entry = {
            "Thumbs": "".join(
                sorted(entry["Thumbs"] + shift_thumb_key + ctrl_thumb_key)
            ),
            "Fingers": entry["Fingers"],
            "Actions": "[KB]"
            + add_modifier(add_modifier(entry_action, shift_label), ctrl_label),
        }
        check_and_add_entry(new_entry)

    if add_shift or add_alt:
        new_entry = {
            "Thumbs": "".join(
                sorted(entry["Thumbs"] + shift_thumb_key + alt_thumb_key)
            ),
            "Fingers": entry["Fingers"],
            "Actions": "[KB]"
            + add_modifier(add_modifier(entry_action, shift_label), alt_label),
        }
        check_and_add_entry(new_entry)

    if add_ctrl or add_alt:
        new_entry = {
            "Thumbs": "".join(sorted(entry["Thumbs"] + ctrl_thumb_key + alt_thumb_key)),
            "Fingers": entry["Fingers"],
            "Actions": "[KB]"
            + add_modifier(add_modifier(entry_action, ctrl_label), alt_label),
        }
        check_and_add_entry(new_entry)

    if add_shift or add_ctrl or add_alt:
        new_entry = {
            "Thumbs": "".join(
                sorted(
                    entry["Thumbs"] + shift_thumb_key + ctrl_thumb_key + alt_thumb_key
                )
            ),
            "Fingers": entry["Fingers"],
            "Actions": "[KB]"
            + add_modifier(
                add_modifier(add_modifier(entry_action, shift_label), ctrl_label),
                alt_label,
            ),
        }
        check_and_add_entry(new_entry)


new_cfg_csv = pd.DataFrame(new_cfg)
new_cfg_csv_file = pathlib.Path(config_csv_file).stem + "_w_modifiers.csv"
new_cfg_csv.to_csv(
    new_cfg_csv_file, index=False, quoting=csv.QUOTE_ALL, doublequote=True
)
