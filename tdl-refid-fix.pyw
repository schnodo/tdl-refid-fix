"""
Based on a backup that is not corrupted, 
tdl-refid-fix restores task references
that were destroyed by ToDoList 8.2.A1.
This comes in handy when the task list was 
worked on for a while before noticing that
references had been destroyed.
"""

import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from lxml import etree


def process_good_TASKs(xml_tree) -> tuple[list, int]:
    """Gather and check REFIDs from the TASK element."""
    tasks_with_refs = []
    tasks = xml_tree.xpath("//TASK")
    for task in tasks:
        id = task.attrib["ID"]
        refid = task.attrib["REFID"]
        if refid != "0":
            tasks_with_refs.append(
                {
                    "id": id,
                    "refid": refid,
                    "task": etree.tostring(task, encoding="UTF-8"),
                }
            )
    return tasks_with_refs, len(tasks_with_refs)


def process_bad_TASKs(good_elements, xml_tree):
    """Replace corrupt tasks with references."""
    tasks = xml_tree.xpath("//TASK")
    for task in tasks:
        if task.attrib["REFID"] == "0":
            for good_element in good_elements:
                if task.attrib["ID"] == good_element["id"]:
                    # Remove illegal characters after the closing tag
                    clean_task = re.sub(
                        r"[^\>]$", "", good_element["task"].decode("utf-8")
                    )
                    task.getparent().replace(task, etree.fromstring(clean_task))
                    continue
    return xml_tree


def main() -> int:
    """Fix REFIDs that were broken by ToDoList 8.2.A1"""
    tk_root = tk.Tk()
    tk_root.withdraw()

    good_tdl_path = filedialog.askopenfilename(
        initialdir=".",
        title="Choose the task list backup with correct task references",
        filetypes=[("Abstractspoon ToDoList", ".tdl")],
    )
    if os.path.isfile(good_tdl_path) == False:
        return 2

    bad_tdl_path = filedialog.askopenfilename(
        initialdir=".",
        title="Choose the task list that is to be repaired",
        filetypes=[("Abstractspoon ToDoList", ".tdl")],
    )
    if os.path.isfile(bad_tdl_path) == False:
        return 2

    # Set working directory
    if os.path.dirname(good_tdl_path):
        os.chdir(os.path.dirname(good_tdl_path))

    xml_parser = etree.XMLParser(remove_blank_text=True)
    # Parse the task list backup that contains working REFIDs
    good_xml_tree = etree.parse(good_tdl_path, xml_parser)

    # Parse the corrupted task list
    bad_xml_tree = etree.parse(bad_tdl_path, xml_parser)

    refids = []
    num_refs = 0

    # Gather tasks with valid REFIDs and patch the corrupted task list
    refids, num_refs = process_good_TASKs(good_xml_tree)
    fixed_xml_tree = process_bad_TASKs(refids, bad_xml_tree)

    fixed_tdl_path = bad_tdl_path.rstrip("tdl").rstrip(".") + "_fixed.tdl"

    with open(fixed_tdl_path, "wb") as doc:
        doc.write(etree.tostring(fixed_xml_tree, pretty_print=True))

    messagebox.showinfo(
        title="Process completed",
        message=f"{str(num_refs)} REFIDs handled.\n",
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
