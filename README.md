# Autoshortcut

Simple Python script to create terminal shortcuts and .desktop files for PyInstaller-built executables. Makes it easy to run Python apps from the terminal or GNOME Activities overview.

## Workflow

1. Create your Python app
2. Run `pyinstaller app_name.py` to build it
3. Run `python autoshortcut.py [options]` to install it

Autoshortcut automatically finds the latest build in the `dist/` directory and creates the necessary symlinks and desktop files.

## Usage

```
python autoshortcut.py [options]
```

### Options

- **No arguments**: Normal install mode
  - Creates a symlink in `/usr/local/bin/` for terminal access
  - If `-d` is also passed, creates a .desktop file for the Activities menu

- **`-d`**: Create a .desktop file
  - Generates a .desktop entry in `~/.local/share/applications/`
  - Can be combined with default install or used with `-o` to create only the desktop file
  - Prompts before overwriting existing files

- **`-o`**: Desktop file only
  - Creates only the .desktop file, skips symlink creation
  - Only meaningful when combined with `-d`

- **`-r`**: Remove/uninstall mode
  - Removes the symlink from `/usr/local/bin/`
  - Removes the .desktop file if it exists

- **`-h`, `--help`**: Show help message and exit

## Examples

```bash
# Normal install: create symlink in /usr/local/bin
python autoshortcut.py

# Create symlink and .desktop file
python autoshortcut.py -d

# Create only .desktop file (no terminal access)
python autoshortcut.py -d -o

# Remove the app installation
python autoshortcut.py -r

# Show help
python autoshortcut.py --help
```

## After Installation

Once installed, you can run your app from the terminal using the executable name:
```bash
app_name
```

If you created a .desktop file with `-d`, the app will also appear in your Activities menu.