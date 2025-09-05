# Roblox Services Cheatsheet

Common services you’ll use often:

- `Workspace`: 3D world containing physical objects
- `Players`: connected players
- `ReplicatedStorage`: shared storage replicated to client and server
- `ServerStorage`: server-only storage (not replicated to clients)
- `StarterPlayer`: holds templates for player characters and scripts
- `StarterGui`: UI templates for players
- `ServerScriptService`: where server `Script`s live
- `StarterPack`: tools given to players on spawn
- `Lighting`: environment settings

Snippets:
```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")
```

Remember: use `:WaitForChild()` when accessing items created elsewhere or by other scripts.
