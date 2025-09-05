# Project 1 — Obby with Checkpoints & Kill Bricks (60–90 min)

Goal: Build a short obby with respawn checkpoints and hazards.

## 1) Layout the course
- Create `Obby` folder in `Workspace`
- Add platforms and obstacles; set `Anchored=true`

## 2) Checkpoints
- Place `SpawnLocation` parts; set `Neutral=true`, `AllowTeamChangeOnTouch=false`
- Add a `Script` in `ServerScriptService` named `Checkpoints`:
```lua
local Players = game:GetService("Players")

Players.PlayerAdded:Connect(function(player)
	player.CharacterAdded:Connect(function(character)
		-- default spawn is fine; updated on touch
	end)
end)

for _, checkpoint in ipairs(workspace.Obby:GetChildren()) do
	if checkpoint:IsA("SpawnLocation") then
		checkpoint.Touched:Connect(function(hit)
			local player = Players:GetPlayerFromCharacter(hit.Parent)
			if not player then return end
			player.RespawnLocation = checkpoint
		end)
	end
end
```

## 3) Kill bricks
- Add thin red Parts named `Kill` under `Obby`; set `Anchored=true`, `CanCollide=true`
- Add a `Script` under each `Kill`:
```lua
local Players = game:GetService("Players")

script.Parent.Touched:Connect(function(hit)
	local player = Players:GetPlayerFromCharacter(hit.Parent)
	if not player then return end
	player:LoadCharacter() -- respawn
end)
```

## 4) Finish part
- Add a `Part` named `Finish` with a `Script`:
```lua
local Players = game:GetService("Players")

script.Parent.Touched:Connect(function(hit)
	local player = Players:GetPlayerFromCharacter(hit.Parent)
	if not player then return end
	print(player.Name .. " finished!")
end)
```

## 5) Polish
- Use `Material`, `Color`, and `Lighting` to make it feel good
- Add a simple timer UI using Lesson 05 patterns

Checkpoint: You respawn at the last checkpoint; red bricks respawn you; finish prints a message.
