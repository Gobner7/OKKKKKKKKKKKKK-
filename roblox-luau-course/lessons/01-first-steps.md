# 01 — First Steps in Roblox Studio (20–30 min)

Goal: Get comfortable with Parts, Explorer, Properties, and run your first scripts (server and client). You’ll also move a Part with code.

## 1) Make a Part and customize it
- Model → Part → Block
- Select it → Properties:
  - Name: `Platform`
  - Color: bright color
  - Size: 10,1,10 (X,Y,Z)

## 2) Organize with folders
- Right click `Workspace` → `Folder` → name `Environment`
- Drag `Platform` into `Environment`

## 3) Your first Script (server-side)
- Right click `ServerScriptService` → `Script` → name `HelloScript`
- Paste:
```lua
print("Server started!")
```
- Play Solo → check Output for the message

## 4) Your first LocalScript (client-side)
- Right click `StarterPlayer` → `StarterPlayerScripts` → `LocalScript`
- Paste:
```lua
print("Hello from the client!")
```
- Play Solo → check Output again

## 5) Move a part with code (simple)
- In `HelloScript`, replace the contents with:
```lua
local part = workspace.Environment.Platform
part.Position = part.Position + Vector3.new(0, 5, 0)
print("Moved platform up by 5 studs")
```
- Play Solo → see it move

## Common errors
- Output not visible: View → Output
- `nil` errors: check names in Explorer (e.g., `Environment` and `Platform` spelled correctly)
- Script vs LocalScript: server code goes in `ServerScriptService`; client code goes in `StarterPlayerScripts`

## Checkpoint
- I can see messages from both server and client in Output
- The platform moves up when I press Play

Next: Lesson 02 — Luau Basics
