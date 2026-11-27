# extsort

A small Python CLI that tidies a messy folder by moving each file into a subfolder named after its extension. Standard library only, one file, nothing to install.

## Why

A Downloads folder fills up with PDFs, notes, and photos all mixed together. `extsort` puts them into `pdf/`, `txt/`, `jpg/`, and so on, and `--dry-run` lets you see the plan before anything moves.

## How to run

Python 3.9 or newer. No third-party packages.

```bash
python3 extsort.py ~/Downloads --dry-run
python3 extsort.py ~/Downloads
```

The folder defaults to the current directory.

- `-n` / `--dry-run` — print the plan and leave files where they are
- `-r` / `--recursive` — also take files from nested folders, then drop them into top-level extension folders

Extensions are lowercased, so `Photo.JPG` goes to `jpg/`. A file with no extension goes to `_no_ext/`. If a file with the same name is already in the destination folder, it is skipped and left where it is (nothing is overwritten). A dry run reports those skips too.

On Windows, use `python extsort.py` instead of `python3 extsort.py`.

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

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
