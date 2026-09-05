-- ObbyLogic: checkpoints, kill parts, launch pads, movers, win pad
-- Behavior driven by StringValue children on parts:
--   Launch = "power"   (launch pad, upward impulse)
--   Spin = "deg/sec"   (spinner, rotates around Y)
--   Slide = "range|speed" (moving platform, oscillates on Z)
--   Conveyor = "speed" (surface velocity on -Z)

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local checkpoints = workspace:WaitForChild("Checkpoints")
local killFolder = workspace:WaitForChild("Kill")
local movers = workspace:WaitForChild("Movers")
local pads = workspace:WaitForChild("Pads")

local stageValues = {} -- [player] = IntValue

Players.PlayerAdded:Connect(function(player)
	local leaderstats = Instance.new("Folder")
	leaderstats.Name = "leaderstats"
	leaderstats.Parent = player

	local stage = Instance.new("IntValue")
	stage.Name = "Stage"
	stage.Value = 0
	stage.Parent = leaderstats
	stageValues[player] = stage

	local timer = Instance.new("NumberValue")
	timer.Name = "Time"
	timer.Value = 0
	timer.Parent = leaderstats

	player.CharacterAdded:Connect(function(char)
		local hrp = char:WaitForChild("HumanoidRootPart")
		task.wait(0.15)
		local st = stage.Value
		if st > 0 then
			local cp = checkpoints:FindFirstChild("Checkpoint" .. st)
			if cp then
				char:PivotTo(cp.CFrame + Vector3.new(0, 4, 0))
			end
		end
	end)
end)

Players.PlayerRemoving:Connect(function(player)
	stageValues[player] = nil
end)

local function getHumanoid(hit)
	local char = hit.Parent
	if not char then return nil, nil end
	local hum = char:FindFirstChildOfClass("Humanoid")
	if not hum then
		hum = char.Parent and char.Parent:FindFirstChildOfClass("Humanoid")
		char = char.Parent
	end
	return hum, char
end

-- Kill parts
for _, p in ipairs(killFolder:GetChildren()) do
	p.Touched:Connect(function(hit)
		local hum = getHumanoid(hit)
		if hum and hum.Health > 0 then
			hum.Health = 0
		end
	end)
end

-- Checkpoints: set stage + teleport on top (debounced)
for _, cp in ipairs(checkpoints:GetChildren()) do
	local idx = tonumber(cp.Name:match("%d+"))
	if idx then
		cp.Touched:Connect(function(hit)
			local hum, char = getHumanoid(hit)
			local plr = char and Players:GetPlayerFromCharacter(char)
			if hum and hum.Health > 0 and plr then
				if char:GetAttribute("CPLock") then return end
				char:SetAttribute("CPLock", true)
				task.delay(1, function()
					if char then char:SetAttribute("CPLock", nil) end
				end)
				local st = stageValues[plr]
				if st and idx > st.Value then
					st.Value = idx
				end
				char:PivotTo(cp.CFrame + Vector3.new(0, 4, 0))
			end
		end)
	end
end

-- Launch pads
for _, pad in ipairs(pads:GetChildren()) do
	local sv = pad:FindFirstChild("Launch")
	if sv then
		local power = tonumber(sv.Value) or 100
		pad.Touched:Connect(function(hit)
			local hum, char = getHumanoid(hit)
			if hum and hum.Health > 0 then
				local hrp = char:FindFirstChild("HumanoidRootPart")
				if hrp then
					local v = hrp.AssemblyLinearVelocity
					hrp.AssemblyLinearVelocity = Vector3.new(v.X, power, v.Z)
				end
			end
		end)
	end
end

-- Movers
for _, m in ipairs(movers:GetChildren()) do
	local spin = m:FindFirstChild("Spin")
	local slide = m:FindFirstChild("Slide")
	local conv = m:FindFirstChild("Conveyor")
	local base = m.CFrame
	if spin then
		local deg = tonumber(spin.Value) or 90
		RunService.Heartbeat:Connect(function(dt)
			m.CFrame = m.CFrame * CFrame.Angles(0, math.rad(deg * dt), 0)
		end)
	elseif slide then
		local range, speed = slide.Value:match("([%d%.]+)|([%d%.]+)")
		range, speed = tonumber(range) or 10, tonumber(speed) or 5
		RunService.Heartbeat:Connect(function()
			local t = os.clock() * speed
			m.CFrame = base * CFrame.new(0, 0, math.sin(t) * range)
		end)
	elseif conv then
		local speed = tonumber(conv.Value) or -8
		m.AssemblyLinearVelocity = Vector3.new(0, 0, speed)
	end
end

-- Win pad
local winPad = workspace:FindFirstChild("WinPad", true)
if winPad then
	winPad.Touched:Connect(function(hit)
		local hum, char = getHumanoid(hit)
		local plr = char and Players:GetPlayerFromCharacter(char)
		if hum and hum.Health > 0 and plr then
			local timer = plr.leaderstats:FindFirstChild("Time")
			if timer and timer.Value == 0 then
				timer.Value = os.clock() - (plr:GetAttribute("StartClock") or os.clock())
				if timer.Value < 0 then timer.Value = 0 end
			end
		end
	end)
end

-- Start clock on spawn
Players.PlayerAdded:Connect(function(player)
	player.CharacterAdded:Connect(function()
		player:SetAttribute("StartClock", os.clock())
	end)
end)

print("ObbyLogic loaded")
