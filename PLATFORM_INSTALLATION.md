# RNA Motif Visualizer - Platform-Specific Installation

Complete step-by-step installation instructions for Windows, macOS, and Linux.

---

## 🍎 macOS Installation

### Step 1: Locate PyMOL Plugins Directory

```bash
# Open Terminal and check if directory exists:
ls -la ~/.pymol/

# If directory doesn't exist, create it:
mkdir -p ~/.pymol/startup/
```

**Expected Output:**
```
total 8
drwxr-xr-x  3 username  staff   96 Dec 10 14:30 .
drwx------+ 24 username staff  768 Dec 10 14:30 ..
drwxr-xr-x  2 username  staff   64 Dec 10 14:30 startup
```

### Step 2: Copy Plugin Folder

```bash
# Navigate to where you downloaded the plugin:
cd ~/Downloads  # or wherever you have it

# Copy the entire rna_motif_visualizer folder:
cp -r rna_motif_visualizer ~/.pymol/startup/

# Verify it was copied:
ls -la ~/.pymol/startup/
```

**Should show:**
```
drwxr-xr-x  7 username  staff  224 Dec 10 14:30 rna_motif_visualizer
```

### Step 3: Set Permissions (if needed)

```bash
# Make sure all files are readable:
chmod -R 755 ~/.pymol/startup/rna_motif_visualizer/

# Verify:
ls -la ~/.pymol/startup/rna_motif_visualizer/
```

### Step 4: Restart PyMOL

```bash
# Close PyMOL completely
# Or in Terminal:
pkill -9 PyMOL

# Reopen PyMOL from Applications
```

### Step 5: Verify Installation

Open PyMOL and in the console, you should see:

```
============================================================
RNA MOTIF VISUALIZER v1.0.0
============================================================
Ready to visualize RNA structural motifs!
```

Test with:
```python
rna_load 1S72
rna_status
```

---

## 🪟 Windows Installation

### Step 1: Find PyMOL Plugins Directory

**Method A: Standard Installation**

```
C:\Program Files\PyMOL\plugins\
```

**Method B: Portable Installation**

```
C:\PyMOL\plugins\
```

**Method C: User AppData** (Most Common)

```
C:\Users\<YourUsername>\AppData\Roaming\PyMOL\startup\
```

**Method D: Find via PyMOL**

Open PyMOL → Click Help → About PyMOL → Look for "Plugins directory"

### Step 2: Create Directory if Needed

If `startup` folder doesn't exist:

1. Right-click in the PyMOL directory
2. Select "New" → "Folder"
3. Name it `startup`

### Step 3: Copy Plugin Folder

1. Locate the downloaded `rna_motif_visualizer` folder
2. Right-click → "Copy"
3. Navigate to your PyMOL startup directory
4. Right-click → "Paste"

**Result should look like:**
```
C:\Users\YourUsername\AppData\Roaming\PyMOL\startup\rna_motif_visualizer\
```

### Step 4: Verify File Structure

Open File Explorer and check:
```
C:\Users\YourUsername\AppData\Roaming\PyMOL\startup\rna_motif_visualizer\
├── __init__.py
├── plugin.py
├── gui.py
├── loader.py
├── colors.py
├── utils\
└── motif_database\
```

### Step 5: Restart PyMOL

1. Close PyMOL completely
2. Wait 5 seconds
3. Reopen PyMOL

### Step 6: Verify Installation

Look for plugin initialization message in PyMOL console. Test:

```python
rna_load 1S72
rna_status
```

---

## 🐧 Linux Installation

### Step 1: Locate PyMOL Plugins Directory

```bash
# Check typical locations:
ls -la ~/.pymol/
ls -la ~/.local/lib/python*/site-packages/pymol/
ls -la ~/pymol/

# Or find PyMOL installation:
which pymol
```

### Step 2: Create/Use PyMOL Startup Directory

**Option A: Home directory (recommended)**

```bash
mkdir -p ~/.pymol/startup/
```

**Option B: System-wide installation**

```bash
# Find your Python site-packages directory:
python -c "import site; print(site.getsitepackages())"

# Should show something like:
# ['/usr/lib/python3.8/site-packages', ...]

# Then navigate to PyMOL plugins:
cd /usr/lib/python3.8/site-packages/pymol/plugins/
```

### Step 3: Copy Plugin Folder

```bash
# For home directory:
cp -r /path/to/rna_motif_visualizer ~/.pymol/startup/

# Verify:
ls -la ~/.pymol/startup/rna_motif_visualizer/
```

### Step 4: Set Permissions

```bash
# Make scripts executable:
chmod -R 755 ~/.pymol/startup/rna_motif_visualizer/

# Verify:
ls -la ~/.pymol/startup/rna_motif_visualizer/
```

### Step 5: Configure PyMOL (if needed)

If using system-wide PyMOL:

```bash
# Edit PyMOL startup file:
nano ~/.pymolrc

# Add this line:
# import pymol.startup

# Save (Ctrl+X, then Y, then Enter)
```

### Step 6: Start PyMOL

```bash
# Start PyMOL from terminal to see any errors:
pymol

# Or in background:
pymol &
```

### Step 7: Verify Installation

In PyMOL console:

```python
rna_load 1S72
rna_status
```

---

## 🔍 Verification Steps (All Platforms)

### Check 1: Plugin Loads
After restarting PyMOL, you should see in console:
```
RNA MOTIF VISUALIZER v1.0.0
```

### Check 2: Commands Registered
In PyMOL console, type:
```python
?rna_load
```

Should show command help (not "unknown command").

### Check 3: Load Structure
```python
rna_load 1S72
```

Should show in console:
```
Loaded structure: 1S72 (PDB: 1S72)
```

### Check 4: Check Status
```python
rna_status
```

Should display something like:
```
Structure: 1S72
PDB ID: 1S72

Loaded Motifs (10):
  KTURN                 ( 2 instances) ✓ visible
  ...
```

### Check 5: Toggle Motifs
```python
rna_toggle KTURN off
rna_toggle KTURN on
```

Red motifs should disappear and reappear in PyMOL window.

---

## ⚠️ Common Issues & Solutions

### Issue: "Plugin doesn't load"

**Windows:**
```
Check: C:\Users\YourUsername\AppData\Roaming\PyMOL\startup\rna_motif_visualizer\
Must have: __init__.py
```

**macOS:**
```
Check: ~/.pymol/startup/rna_motif_visualizer/
Run: ls -la ~/.pymol/startup/
Must show: rna_motif_visualizer folder
```

**Linux:**
```
Check: ~/.pymol/startup/rna_motif_visualizer/
Run: ls -la ~/.pymol/startup/
Must show: rna_motif_visualizer folder
```

**Solution:**
1. Verify folder structure is complete
2. Ensure `__init__.py` exists in folder
3. Check file permissions
4. Restart PyMOL completely

### Issue: "rna_load command not found"

**Solution:**
1. Restart PyMOL completely (close and reopen)
2. Check PyMOL console for error messages
3. Verify plugin folder location
4. Check file permissions

### Issue: "Permission denied" (macOS/Linux)

**macOS:**
```bash
chmod -R 755 ~/.pymol/startup/rna_motif_visualizer/
```

**Linux:**
```bash
chmod -R 755 ~/.pymol/startup/rna_motif_visualizer/
```

### Issue: PyMOL doesn't start after installation

**Solution:**
1. Check PyMOL console for error messages
2. Verify Python compatibility (PyMOL needs Python 2.7+ or 3.5+)
3. Try in safe mode (if available)
4. Reinstall plugin from scratch

---

## 🗂️ Folder Location Reference

| OS | Path |
|----|------|
| **macOS** | `~/.pymol/startup/` |
| **Windows (AppData)** | `C:\Users\<Name>\AppData\Roaming\PyMOL\startup\` |
| **Windows (Program Files)** | `C:\Program Files\PyMOL\plugins\` |
| **Linux** | `~/.pymol/startup/` |

---

## ✅ Final Verification Checklist

### Before Installation
- [ ] Downloaded the plugin folder
- [ ] Know your PyMOL plugins directory location
- [ ] Have write permissions to that directory

### During Installation
- [ ] Copied `rna_motif_visualizer` folder to correct location
- [ ] Verified folder structure is complete
- [ ] Set proper permissions (755 on macOS/Linux)

### After Installation
- [ ] Restarted PyMOL
- [ ] Saw initialization message in console
- [ ] Can run: `rna_load 1S72`
- [ ] Can run: `rna_status`
- [ ] Can run: `rna_toggle KTURN on`

### Troubleshooting
- [ ] Checked file permissions
- [ ] Verified all files copied
- [ ] Checked Python version in PyMOL
- [ ] Restarted PyMOL after changes

---

## 🆘 Getting Help

### If Installation Fails

1. **Check Error Message**
   - Open PyMOL console (Windows → Python Console)
   - Look for red error text
   - Note exact error message

2. **Verify File Structure**
   - Ensure `__init__.py` exists in plugin folder
   - Ensure `motif_database/` folder exists with JSON files
   - Ensure `utils/` folder exists

3. **Check Permissions** (macOS/Linux)
   ```bash
   chmod -R 755 ~/.pymol/startup/rna_motif_visualizer/
   ```

4. **Restart Everything**
   - Close PyMOL completely
   - Wait 5 seconds
   - Reopen PyMOL
   - Try again

### If Commands Don't Work

1. Make sure PyMOL fully loaded (watch console)
2. Try: `?rna_load` (should show help)
3. Restart PyMOL if that doesn't work
4. Check console for any error messages

### If No Motifs Load

- Not all PDB IDs have motif annotations in database
- Try: `rna_load 1S72` (known to have motifs)
- Check with: `rna_status`
- Add your own motifs (see main README)

---

## 🎯 Next Steps After Installation

1. ✅ Installation complete
2. 📖 Read: `USAGE_EXAMPLES.md` for examples
3. 🚀 Try: `rna_load 1S72` and explore
4. 📚 Learn: Check `rna_motif_visualizer/README.md` for full docs
5. 🔧 Extend: Add your own motifs (optional)

---

## Platform-Specific Tips

### macOS Tips
- Use Terminal for file operations
- Homebrew PyMOL: Plugins in `/usr/local/share/pymol/`
- Use `open ~/.pymol` to open folder in Finder

### Windows Tips
- Use File Explorer (not Command Prompt) for file operations
- AppData folder is hidden by default
- Enable "Show hidden files" to see it
- Use forward slashes (/) in PyMOL paths

### Linux Tips
- Use `ls -la` to see hidden files
- Use `chmod` for permission changes
- PyMOL might be in `/opt/pymol/`
- Use `which pymol` to find installation

---

**Installation Complete!** Now read `USAGE_EXAMPLES.md` to get started! 🎉
