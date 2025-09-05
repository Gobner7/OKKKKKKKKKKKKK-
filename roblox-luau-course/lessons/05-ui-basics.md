# 05 — UI Building with ScreenGui and Buttons (25–35 min)

Goal: Create a simple UI with a button that fires an event.

## 1) Build the UI
- `StarterGui` → `ScreenGui` → name `MainGui`
- Inside `MainGui` → `TextButton` → name `PingButton`
- Set Properties:
  - Text: `Ping`
  - Size: {0, 120},{0, 40}
  - Position: {0.05, 0},{0.85, 0}

## 2) Wire the button (client)
- `PingButton` → `LocalScript`
```lua
local button = script.Parent
button.MouseButton1Click:Connect(function()
	print("Button clicked")
end)
```

## 3) Connect to RemoteEvent (optional if done Lesson 04)
- In the same LocalScript:
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local Ping = Remotes:WaitForChild("Ping")

button.MouseButton1Click:Connect(function()
	Ping:FireServer("Ping from UI")
end)
```

## 4) Practice
- Change the button color on hover (`MouseEnter` / `MouseLeave`)
- Add a `TextLabel` that shows the last server time using `GetTime`

Common errors: UI not visible? Ensure `ScreenGui` is in `StarterGui`, and not disabled.

Next: Project 1 — Obby
