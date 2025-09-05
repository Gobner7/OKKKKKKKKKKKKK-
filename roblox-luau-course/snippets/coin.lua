-- Place a Part named Coin in Workspace, attach this as a Script
local Players = game:GetService("Players")

script.Parent.Touched:Connect(function(hit)
	local character = hit.Parent
	if not character then return end
	local player = Players:GetPlayerFromCharacter(character)
	if not player then return end

	local leaderstats = player:FindFirstChild("leaderstats")
	if not leaderstats then return end
	local Coins = leaderstats:FindFirstChild("Coins")
	if not Coins then return end

	Coins.Value += 1
	script.Parent:Destroy()
end)
