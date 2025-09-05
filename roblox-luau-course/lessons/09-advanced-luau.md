# 09 — Advanced Luau: Types, Modules, OOP Pattern (45–60 min)

Goal: Use Luau type annotations, create a ModuleScript, and implement a simple OOP pattern.

## 1) Type annotations
```lua
local function add(a: number, b: number): number
	return a + b
end

local user: {name: string, coins: number} = { name = "Alex", coins = 0 }
```

## 2) ModuleScript basics
- `ReplicatedStorage` → `ModuleScript` named `Utils`:
```lua
local Utils = {}

function Utils.round(n: number, decimals: number): number
	local power = 10 ^ decimals
	return math.floor(n * power + 0.5) / power
end

return Utils
```

- Using the module:
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Utils = require(ReplicatedStorage:WaitForChild("Utils"))
print(Utils.round(3.14159, 2)) -- 3.14
```

## 3) OOP pattern with metatables
- `ReplicatedStorage` → `ModuleScript` named `CoinPurse`:
```lua
export type CoinPurse = {
	coins: number,
	Add: (self: CoinPurse, amount: number) -> (),
	Spend: (self: CoinPurse, amount: number) -> boolean,
}

local CoinPurse = {}
CoinPurse.__index = CoinPurse

function CoinPurse.new(initial: number): CoinPurse
	local self = setmetatable({ coins = initial or 0 }, CoinPurse)
	return self
end

function CoinPurse:Add(amount: number)
	self.coins += amount
end

function CoinPurse:Spend(amount: number): boolean
	if self.coins >= amount then
		self.coins -= amount
		return true
	end
	return false
end

return CoinPurse
```

- Using it:
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local CoinPurse = require(ReplicatedStorage:WaitForChild("CoinPurse"))

local purse = CoinPurse.new(10)
purse:Add(5)
print("Coins:", purse.coins)
print("Bought?", purse:Spend(12))
print("Coins:", purse.coins)
```

Next: Lesson 10 — Polish, Testing, Publishing
