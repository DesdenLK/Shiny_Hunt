local TRAINER_TID = 40665
local TRAINER_SID = 6348

local ROAMER_BASE = 0x02028878

callbacks:add("frame", function()
    local ivs         = emu:read32(ROAMER_BASE + 0x00)
    local pid         = emu:read32(ROAMER_BASE + 0x04)
    local species     = emu:read16(ROAMER_BASE + 0x08)
    local hp          = emu:read16(ROAMER_BASE + 0x0A)
    local level       = emu:read8 (ROAMER_BASE + 0x0C)
    local status      = emu:read8 (ROAMER_BASE + 0x0D)
    local cool        = emu:read8 (ROAMER_BASE + 0x0E)
    local beauty      = emu:read8 (ROAMER_BASE + 0x0F)
    local cute        = emu:read8 (ROAMER_BASE + 0x10)
    local smart       = emu:read8 (ROAMER_BASE + 0x11)
    local tough       = emu:read8 (ROAMER_BASE + 0x12)
    local active      = emu:read8 (ROAMER_BASE + 0x13)

    local mapBank     = emu:read8(0x02037EF0)
    local mapId       = emu:read8(0x02037EF1)

    local sv = (TRAINER_TID ~ TRAINER_SID ~ (pid >> 16) ~ (pid & 0xFFFF)) & 0xFFFF
    local isShiny = sv < 8

    console:log(string.format("--- Roamer ---"))
    console:log(string.format("Species:%d  Level:%d  HP:%d", species, level, hp))
    console:log(string.format("PID:0x%08X  IVs:0x%08X", pid, ivs))
    console:log(string.format("SV:%d  Shiny:%s", sv, tostring(isShiny)))
    console:log(string.format("Status:%d  Active:%d", status, active))
    console:log(string.format("Contest: Cool:%d Beauty:%d Cute:%d Smart:%d Tough:%d", cool, beauty, cute, smart, tough))
    console:log(string.format("Map: Bank:%d Id:%d", mapBank, mapId))
end)