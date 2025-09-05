# 08 — Data Saving Basics with DataStoreService (35–50 min)

Goal: Save and load a single stat (Coins) safely.

## 1) Enable API access
- Home → Game Settings → Security → Enable Studio Access to API Services

## 2) Server script: save/load coins
- `ServerScriptService` → `Script` named `SaveCoins`:
```lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local coinsStore = DataStoreService:GetDataStore("CoinsV1")

local function getKey(userId: number): string
	return "coins_" .. tostring(userId)
end

local function safelyGet(defaultValue)
	return function(callback)
		local success, result = pcall(callback)
		if success then return result end
		warn("DataStore get failed:", result)
		return defaultValue
	end
end

local function safelyCall(callback)
	local success, err = pcall(callback)
	if not success then warn("DataStore call failed:", err) end
end

Players.PlayerAdded:Connect(function(player)
	local key = getKey(player.UserId)
	local saved = safelyGet(0)(function()
		return coinsStore:GetAsync(key)
	end)

	local leaderstats = Instance.new("Folder")
	leaderstats.Name = "leaderstats"
	leaderstats.Parent = player

	local Coins = Instance.new("IntValue")
	Coins.Name = "Coins"
	Coins.Value = saved or 0
	Coins.Parent = leaderstats
end)

Players.PlayerRemoving:Connect(function(player)
	local key = getKey(player.UserId)
	local coins = player:FindFirstChild("leaderstats") and player.leaderstats:FindFirstChild("Coins")
	local value = coins and coins.Value or 0
	safelyCall(function()
		coinsStore:SetAsync(key, value)
	end)
end)
```

## 3) Test
- Play Solo, earn coins, stop play, start again — the value should persist

Common errors: “Request throttled” — avoid saving too frequently; only save on `PlayerRemoving` and major milestones.

Next: Lesson 09 — Advanced Luau
