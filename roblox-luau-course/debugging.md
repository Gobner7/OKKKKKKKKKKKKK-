# Debugging & Common Errors

## Read errors out loud
- Errors tell you the file, line, and message. Read it slowly.

## Output window
- View → Output. Use `print()` to confirm values and flow.

## Common issues
- `attempt to index nil`: the variable is nil — `print()` it; check names; use `WaitForChild` for instances
- RemoteEvent not firing: check it’s in `ReplicatedStorage/Remotes` and names match; client uses `:FireServer`, server listens on `OnServerEvent`
- LocalScript not running: must be in a client context (`StarterPlayerScripts`, `StarterGui`, inside a PlayerGui/Tool)
- Script not running: server Scripts run in `ServerScriptService` or under server-owned objects
- `Infinite yield` from `WaitForChild`: the child never appeared — ensure another script creates it or create it yourself
- Physics weirdness: set Parts `Anchored` or `CanCollide` properly

## Strategy
1) Reproduce the bug in the smallest steps
2) Print values before and after the failing line
3) Check the Explorer names carefully
4) Comment out questionable code to isolate the issue

## Checklist before asking for help
- What did you expect vs what happened?
- Relevant script names, locations, and error messages
- Minimal code snippet that reproduces the bug
