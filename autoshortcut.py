#!/usr/bin/env python3
import os
import glob
import sys

# Flags
make_desktop = "-d" in sys.argv
remove_install = "-r" in sys.argv

# 1️ Locate the latest build in dist/
dist_path = os.path.join(os.getcwd(), "dist")
if not os.path.exists(dist_path):
    raise FileNotFoundError("dist/ folder not found. Run PyInstaller first.")

subdirs = [d for d in glob.glob(os.path.join(dist_path, "*")) if os.path.isdir(d)]
if not subdirs:
    raise FileNotFoundError("No build folders found in dist/")

latest_build = max(subdirs, key=os.path.getmtime)
exe_name = os.path.basename(latest_build)

# Paths used for install/removal
symlink_path = f"/usr/local/bin/{exe_name}"
desktop_path = os.path.expanduser(f"~/.local/share/applications/{exe_name}.desktop")

# --- REMOVE MODE (-r) ---
if remove_install:
    removed_anything = False

    if os.path.islink(symlink_path) or os.path.exists(symlink_path):
        print(f"Removing symlink: {symlink_path}")
        os.system(f"sudo rm {symlink_path}")
        removed_anything = True
    else:
        print("No symlink found.")

    if os.path.exists(desktop_path):
        print(f"Removing .desktop file: {desktop_path}")
        os.remove(desktop_path)
        removed_anything = True
    else:
        print("No .desktop file found.")

    if removed_anything:
        print("Removal complete.")
    else:
        print("Nothing to remove.")

    sys.exit(0)

# --- NORMAL INSTALL MODE ---

# Find the executable inside the build folder
files = [
    f for f in glob.glob(os.path.join(latest_build, "*"))
    if os.path.isfile(f) and not os.path.basename(f).startswith(".")
]

if not files:
    raise FileNotFoundError(f"No executable found in {latest_build}")

exe_path = os.path.abspath(files[0])

# 2 Create .desktop file only if -d is passed
if make_desktop:
    icon_path = "/usr/share/icons/gnome/32x32/status/network-transmit.png"
    desktop_contents = f"""[Desktop Entry]
Name={exe_name}
Comment=Run {exe_name}
Exec={exe_path}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Utility;
"""

    if os.path.exists(desktop_path):
        response = input(
            f"A .desktop file for '{exe_name}' already exists. Overwrite? [y/N]: "
        ).strip().lower()
        if response != "y":
            print("Skipped .desktop creation.")
        else:
            with open(desktop_path, "w") as f:
                f.write(desktop_contents)
            os.chmod(desktop_path, 0o755)
            print(f".desktop file overwritten: {desktop_path}")
    else:
        with open(desktop_path, "w") as f:
            f.write(desktop_contents)
        os.chmod(desktop_path, 0o755)
        print(f".desktop file created: {desktop_path}")

# 3 Create symlink in /usr/local/bin (always)
if os.path.exists(symlink_path):
    response = input(
        f"A file or command named '{exe_name}' already exists in /usr/local/bin. Overwrite? [y/N]: "
    ).strip().lower()
    if response != "y":
        print("Skipped creating symlink.")
    else:
        os.system(f"sudo rm {symlink_path}")
        os.system(f"sudo ln -s {exe_path} {symlink_path}")
        print(f"Symlink overwritten: {symlink_path} -> {exe_path}")
else:
    os.system(f"sudo ln -s {exe_path} {symlink_path}")
    print(f"Symlink created: {symlink_path} -> {exe_path}")

print(f"You can now run your app from the terminal: {exe_name}")
