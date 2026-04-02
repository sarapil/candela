#!/usr/bin/env python3
"""Copy `desktop_utils.py` from `apps/candela/candela/desktop_utils.py` into each app package directory.

Usage:
    python3 copy_desktop_utils_to_apps.py

This will:
- iterate /workspace/development/frappe-bench/apps
- for each folder `X` where `apps/X/X/` exists, copy the source utility if target doesn't exist
- skip apps where the target already exists
- print a summary
"""
import os, shutil, sys

BENCH_APPS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apps')
SRC = os.path.join(BENCH_APPS_DIR, 'candela', 'candela', 'desktop_utils.py')

if not os.path.exists(SRC):
    print('Source desktop_utils.py not found at', SRC)
    sys.exit(1)

copied = []
skipped = []
errors = []

for app_name in sorted(os.listdir(BENCH_APPS_DIR)):
    app_dir = os.path.join(BENCH_APPS_DIR, app_name)
    if not os.path.isdir(app_dir):
        continue
    # target package dir e.g. apps/arrowz/arrowz
    target_pkg = os.path.join(app_dir, app_name)
    if not os.path.isdir(target_pkg):
        # some apps have different layout; try find first python package dir
        candidates = [d for d in os.listdir(app_dir) if os.path.isdir(os.path.join(app_dir, d)) and os.path.exists(os.path.join(app_dir, d, '__init__.py'))]
        if candidates:
            target_pkg = os.path.join(app_dir, candidates[0])
        else:
            skipped.append((app_name, 'no package dir'))
            continue

    target_file = os.path.join(target_pkg, 'desktop_utils.py')
    try:
        if os.path.exists(target_file):
            skipped.append((app_name, 'exists'))
            continue
        shutil.copy2(SRC, target_file)
        copied.append(app_name)
    except Exception as e:
        errors.append((app_name, str(e)))

print('Copied to apps:')
for c in copied:
    print('  ', c)
print('\nSkipped:')
for s in skipped:
    print('  ', s[0], '-', s[1])

if errors:
    print('\nErrors:')
    for e in errors:
        print('  ', e[0], '-', e[1])

print('\nDone')
