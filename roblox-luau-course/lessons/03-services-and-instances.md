# 03 — Roblox Services and Instances (25–35 min)

Goal: Learn core services (Workspace, Players, ReplicatedStorage) and create/find instances in code.

## 1) Find services
```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")
print(Players, ReplicatedStorage, Workspace)
```

## 2) Create instances and parent them
```lua
local folder = Instance.new("Folder")
folder.Name = "MyFolder"
folder.Parent = Workspace

local part = Instance.new("Part")
part.Name = "MovingPart"
part.Size = Vector3.new(4,1,4)
part.Position = Vector3.new(0, 3, 0)
part.Parent = folder
```

## 3) Wait for children safely
```lua
local environment = Workspace:WaitForChild("Environment")
local platform = environment:WaitForChild("Platform")
print("Found:", platform)
```

## 4) ReplicatedStorage for shared assets
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Create a shared RemoteEvent for later lessons
local RemoteEvent = Instance.new("RemoteEvent")
RemoteEvent.Name = "Ping"
RemoteEvent.Parent = ReplicatedStorage
```

## 5) Practice
- Create a folder `Spawned` in `Workspace` and spawn 5 parts in a row using a loop
- Extra: randomize color using `BrickColor.random()`

Common errors: `nil` from `FindFirstChild` — the item doesn’t exist; use `WaitForChild` when created elsewhere.

Next: Lesson 04 — Client-Server with RemoteEvents/Functions
