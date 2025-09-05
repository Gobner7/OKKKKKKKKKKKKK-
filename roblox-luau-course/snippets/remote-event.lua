-- Setup: ReplicatedStorage/Remotes/Ping (RemoteEvent)
-- Server (ServerScriptService)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local Ping = Remotes:WaitForChild("Ping")

Ping.OnServerEvent:Connect(function(player, msg)
	print("Ping:", player.Name, msg)
end)

-- Client (StarterPlayerScripts/LocalScript)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local Ping = Remotes:WaitForChild("Ping")

Ping:FireServer("Hello!")
