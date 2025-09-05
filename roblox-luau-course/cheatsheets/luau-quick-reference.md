# Luau Quick Reference

## Variables
```lua
local x = 10
local name = "Alex"
```

## Tables
```lua
local arr = {1,2,3}
local dict = {health = 100, speed = 16}
```

## Functions
```lua
local function add(a, b)
	return a + b
end
```

## Conditionals
```lua
if x > 5 then
	print("big")
elseif x == 5 then
	print("equal")
else
	print("small")
end
```

## Loops
```lua
for i = 1, 5 do print(i) end
local i = 0
while i < 5 do i += 1 end
```

## Type Annotations (preview)
```lua
local function add(a: number, b: number): number
	return a + b
end

local playerName: string = "Alex"
```

## Modules
```lua
-- ModuleScript returns a table
local M = {}
function M.greet(name)
	print("Hi", name)
end
return M
```

Tips: arrays start at 1; use `WaitForChild` when referencing instances created elsewhere.
