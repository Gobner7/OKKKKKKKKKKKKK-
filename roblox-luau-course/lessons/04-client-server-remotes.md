# 04 — Client-Server with RemoteEvents/Functions (35–45 min)

Goal: Send messages between client and server using RemoteEvent and RemoteFunction.

Setup: In `ReplicatedStorage`, create a `Folder` named `Remotes` and inside it add a `RemoteEvent` named `Ping` and a `RemoteFunction` named `GetTime`.

## 1) Server: listen for RemoteEvent
- `ServerScriptService` → `Script` → `RemotesServer`
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local Ping = Remotes:WaitForChild("Ping")

Ping.OnServerEvent:Connect(function(player, message)
	print("Ping from", player.Name, "message:", message)
end)
```

## 2) Client: fire RemoteEvent
- `StarterPlayerScripts` → `LocalScript` → `RemotesClient`
```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local Ping = Remotes:WaitForChild("Ping")

Ping:FireServer("Hello server!")
```
- Play Solo → check Output on server

## 3) RemoteFunction: request/response
- Server handler in `RemotesServer`:
```lua
local GetTime = Remotes:WaitForChild("GetTime")
GetTime.OnServerInvoke = function(player)
	return os.time()
end
```
- Client caller in `RemotesClient`:
```lua
local GetTime = Remotes:WaitForChild("GetTime")
local t = GetTime:InvokeServer()
print("Server time:", t)
```

## Common errors
- `Attempt to call nil` on RemoteFunction: ensure `OnServerInvoke` is set
- Typos in names: verify `Remotes`, `Ping`, `GetTime` exist in `ReplicatedStorage`

Next: Lesson 05 — UI Building
