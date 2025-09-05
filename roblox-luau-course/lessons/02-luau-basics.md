# 02 — Luau Basics (30–45 min)

Goal: Learn variables, types-by-example, tables (arrays/dictionaries), functions, if/else, loops.

Open a `Script` in `ServerScriptService` named `Basics` and try each section.

## 1) Variables and printing
```lua
local playerName = "Alex"
local coins = 0
print("Player:", playerName, "Coins:", coins)
```

## 2) Tables — arrays and dictionaries
```lua
-- Array
local colors = {"Red", "Green", "Blue"}
print(colors[1]) -- Red

-- Dictionary
local stats = {health = 100, speed = 16}
print(stats.health)

-- Mixed
local inventory = {
	{ name = "Coin", amount = 5 },
	{ name = "Potion", amount = 1 },
}
print(inventory[2].name)
```

## 3) Functions and returning values
```lua
local function add(a, b)
	return a + b
end

local total = add(5, 7)
print("Total:", total)
```

## 4) If/else and loops
```lua
local lives = 3
if lives > 0 then
	print("Alive")
else
	print("Game Over")
end

-- for loop
for i = 1, 5 do
	print("i =", i)
end

-- while loop
local n = 3
while n > 0 do
	print("n =", n)
	n = n - 1
end
```

## 5) Practice: greet and count
- Write a function `greet(name)` that prints `Hello, <name>`
- Use a `for` loop to count from 10 down to 1, then print `Go!`

## Common errors
- `nil` indexing: table[key] doesn’t exist — print your table to check keys
- Off-by-one: arrays start at index 1 in Luau

Next: Lesson 03 — Roblox Services and Instances
