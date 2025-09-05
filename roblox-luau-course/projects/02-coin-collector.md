# Project 2 — Coin Collector with Leaderstats & Shop (90–120 min)

Goal: Spawn coins, collect them, display leaderstats, and spend in a simple shop.

## 1) Leaderstats (reuse snippet)
- Use `snippets/leaderstats.lua`

## 2) Coin spawner
- `ServerScriptService` → `Script` named `CoinSpawner`:
```lua
local Workspace = game:GetService("Workspace")

local function spawnCoin(position: Vector3)
	local coin = Instance.new("Part")
	coin.Name = "Coin"
	coin.Shape = Enum.PartType.Ball
	coin.Size = Vector3.new(1,1,1)
	coin.BrickColor = BrickColor.new("Bright yellow")
	coin.Anchored = true
	coin.Position = position
	coin.Parent = Workspace

	local touch = Instance.new("Script")

touch.Source = [[
local Players = game:GetService("Players")
script.Parent.Touched:Connect(function(hit)
	local player = Players:GetPlayerFromCharacter(hit.Parent)
	if not player then return end
	local ls = player:FindFirstChild("leaderstats")
	local Coins = ls and ls:FindFirstChild("Coins")
	if Coins then Coins.Value += 1 end
	script.Parent:Destroy()
end)
]]

touch.Parent = coin
end

for i = 1, 20 do
	spawnCoin(Vector3.new(i*3, 2, 0))
end
```

## 3) Shop UI
- `StarterGui` → `ScreenGui` (`ShopGui`) → `TextButton` (`BuySpeed`)
- LocalScript under `BuySpeed`:
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local BuySpeed = Remotes:FindFirstChild("BuySpeed") or Instance.new("RemoteEvent", Remotes)
BuySpeed.Name = "BuySpeed"

local button = script.Parent
button.Text = "Buy +4 WalkSpeed (5 Coins)"

button.MouseButton1Click:Connect(function()
	BuySpeed:FireServer()
end)
```

## 4) Shop server handler
- `ServerScriptService` → `Script`:
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local Remotes = ReplicatedStorage:FindFirstChild("Remotes") or Instance.new("Folder", ReplicatedStorage)
Remotes.Name = "Remotes"
local BuySpeed = Remotes:FindFirstChild("BuySpeed") or Instance.new("RemoteEvent", Remotes)
BuySpeed.Name = "BuySpeed"

BuySpeed.OnServerEvent:Connect(function(player)
	local ls = player:FindFirstChild("leaderstats")
	local Coins = ls and ls:FindFirstChild("Coins")
	if not Coins then return end
	if Coins.Value >= 5 then
		Coins.Value -= 5
		local character = player.Character or player.CharacterAdded:Wait()
		local humanoid = character:WaitForChild("Humanoid")
		humanoid.WalkSpeed += 4
		print(player.Name .. " bought speed!")
	else
		print("Not enough coins")
	end
end)
```

Checkpoint: Coins spawn and can be collected; leaderstats show coins; shop buys speed for 5 coins.

Next: Lesson 08 — Data saving basics
