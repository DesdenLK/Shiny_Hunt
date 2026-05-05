local TRAINER_TID = 30764
local TRAINER_SID = 7445

callbacks:add("frame", function()
    local base = 0x0202887C

    local pid     = emu:read32(base + 0x00)
    local species = emu:read16(base + 0x04)
    local level      = emu:read16(base + 0x08)

    local sv = (TRAINER_TID ~ TRAINER_SID ~ (pid >> 16) ~ (pid & 0xFFFF)) & 0xFFFF

    console:log(string.format("Species:%d Level:%d", species, level))
    console:log(string.format("PID:0x%08X SV:%d Shiny:%s", pid, sv, tostring(sv < 8)))
end)