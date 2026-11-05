# extsort

Tiny Python CLI that sorts files in a folder into subfolders by extension.

Example: `report.pdf`, `notes.txt`, and `photo.jpg` in `Downloads/` become `pdf/`, `txt/`, and `jpg/`.

## Requirements

- Python 3.9+
- No third-party packages

## Usage

```bash
python extsort.py ~/Downloads --dry-run
python extsort.py ~/Downloads
```

Options:

- `-n` / `--dry-run` — print the plan without moving files
- `-r` / `--recursive` — also pick up files in nested folders (still drops them into top-level extension folders)

Files with no extension go into `_no_ext/`. Existing destination files are skipped.

## Why

I keep dumping mixed files into one folder. This is the smallest script that cleans that up without asking me to install anything.
