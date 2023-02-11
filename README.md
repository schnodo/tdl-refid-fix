# tdl-refid-fix
Based on a backup that is not corrupted, tdl-refid-fix restores task references that were destroyed by ToDoList 8.2.A1. This comes in handy when the task list was  worked on for a while before noticing that references had been replaced by plain copies.

The implementation does not provide a lot of error handling. I really needed the tool only once to reconstruct a large number of destroyed references.

## How to use
1. Using Python, run `tdl-refid-fix.pyw`
1. Select the file that contains the backup (good), with the references still existing.
1. Select the file where the references are destroyed (bad).

## What it does
1. tdl-refid-fix identifies all tasks in the good file that have a `REFID` that differs from 0. For those, it stores the task element.
1. tdl-refid-fix then goes through the bad file and compares the "bad" task `IDs` with the "good" task `IDs`.
1. tdl-refid-fix there is a match, it replaces the bad element with the corresponding good element.
1. tdl-refid-fix saves the file. If the bad file name is `bad.tdl`, the corrected file will be saved as `bad_fixed.tdl`.

## Things to consider
If you manually arranged the tasks in `bad.tdl`, rename `bad_fixed.tdl` to `bad.tdl` after assuring its correctness. Otherwise the order set by the user seems to get lost.
