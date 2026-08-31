# pypipup

Too lazy to check which Python packages are outdated?

Same.

`pypipup` is a small command-line utility for checking the packages installed in your current Python environment and updating them when you actually want to.

The important part: **it does not update anything by default anymore**.

Running:

```bash
pypipup
```

just shows you what's outdated.

For example:

```text
3 update(s) available:

  httpx  0.27.0 → 0.28.1
  rich   13.8.0 → 13.9.4
  ruff   0.8.0  → 0.9.2
```

You decide what happens next.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/niCodeLine/pypipup.git
cd pypipup
```

Then install it in your environment:

```bash
python -m pip install -e .
```

Or just copy the module into your project if that's what you prefer.

---

## Usage

### Check for updates

Just run:

```bash
pypipup
```

This is the safe/default mode.

It checks the packages installed in the **currently active Python environment** and shows which ones have newer versions available.

Nothing gets modified.

---

## Apply updates

If everything looks fine:

```bash
pypipup --apply
```

pypipup will show you the planned updates and ask for confirmation before touching anything.

Because automatically upgrading your entire Python environment without asking is... perhaps not the greatest idea I ever had.

---

## Skip the confirmation

If you already know what you're doing:

```bash
pypipup --apply --yes
```

Useful for scripts or environments where you don't want the confirmation prompt.

---

## Exclude packages

Sometimes you absolutely do **not** want to update a particular dependency.

For example:

```bash
pypipup --apply --exclude numpy
```

You can combine options:

```bash
pypipup --apply --yes --exclude numpy
```

So pypipup can update everything else while leaving NumPy alone.

---

## Clean pip's cache

You can also purge pip's cache after updating:

```bash
pypipup --apply --purge-cache
```

Or go full housekeeping mode:

```bash
pypipup --apply --yes --exclude numpy --purge-cache
```

---

## JSON output

If another script wants to use the results instead of your eyes:

```bash
pypipup --json
```

This produces machine-readable output instead of the normal terminal presentation.

Useful for automation, other Python tools, or whatever questionable pipeline you are building.

---

## Safety

The original idea behind pypipup was basically:

> find old packages → update everything → hope

It now behaves a little more responsibly.

### Preview first

Running:

```bash
pypipup
```

never changes your environment.

Updates only happen with:

```bash
pypipup --apply
```

### Confirmation before updates

Even with `--apply`, pypipup asks before actually upgrading anything unless you explicitly pass:

```bash
--yes
```

### Uses your active Python

pypipup uses the same Python interpreter that launched it.

That means if you're inside:

```text
.venv
```

it checks and updates packages **inside that environment**, instead of randomly messing with another Python installation on your machine.

### No shell-command nonsense

Package names are passed safely to subprocesses instead of being assembled into shell commands.

### Failed updates are reported

If some packages update successfully and another fails, pypipup reports the partial failure and exits with a non-zero status instead of pretending everything went perfectly.

---

## A small warning

Updating every package at once can break things.

For little personal environments, experimentation, or development, that's often perfectly manageable.

For something important, it is better to:

- use a virtual environment
- review major version changes
- keep reproducible dependency versions
- test after updating

In other words: pypipup can press the buttons for you, but it cannot make dependency compatibility cease to exist.

---

## Features

- **Check outdated packages**
- **Preview updates without modifying anything**
- **Update packages on request**
- **Confirmation before changes**
- **Automatic confirmation with `--yes`**
- **Exclude specific packages**
- **Optional pip cache cleanup**
- **JSON output**
- **Uses the active Python environment**
- **Reports failed or partial updates properly**
- **No runtime dependencies beyond Python/pip**

---

## Development

```bash
python -m pip install -e ".[dev]"

pytest
ruff check .
```

---

## Contributions

If you find a bug, have an improvement, or pip invents another interesting way of making package management annoying, feel free to open an issue or send a pull request.

---

## License

MIT © Nico Spok

Do whatever you want. 