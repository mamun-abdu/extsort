# extsort

Small Python 3.9+ CLI that sorts the files in a folder into subfolders named by extension. Standard library only.

## Problem

One folder fills up with PDFs, notes, and photos mixed together. This moves each file into a folder named for its extension, with nothing to install.

## How to run

Python 3.9 or newer. No third-party packages.

```bash
python3 extsort.py ~/Downloads --dry-run
python3 extsort.py ~/Downloads
```

The folder defaults to the current directory.

- `-n` / `--dry-run` — print the plan and leave files where they are
- `-r` / `--recursive` — also take files from nested folders, then drop them into top-level extension folders

Extensions are lowercased. A file with no extension goes to `_no_ext/`. If that name already exists in the destination, the file is skipped.

## Example

Before:

```text
Downloads/
├── notes.txt
├── report.pdf
├── photo.jpg
└── README
```

```bash
python3 extsort.py Downloads --dry-run
```

```text
would move: notes.txt -> txt/
would move: report.pdf -> pdf/
would move: photo.jpg -> jpg/
would move: README -> _no_ext/
Would sort 4 file(s).
```

After a real run, the same folder looks like this:

```text
Downloads/
├── jpg/photo.jpg
├── pdf/report.pdf
├── txt/notes.txt
└── _no_ext/README
```

Running it again prints `Nothing to sort.`

## License

MIT. See [LICENSE](LICENSE).
