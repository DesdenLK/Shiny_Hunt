local function r8(addr)  return emu:read8(addr) or 0 end
local function r16(addr) return emu:read16(addr) or 0 end
local function r32(addr) return emu:read32(addr) or 0 end

local orders = {
    {1,2,3,4},{1,2,4,3},{1,3,2,4},{1,3,4,2},{1,4,2,3},{1,4,3,2},
    {2,1,3,4},{2,1,4,3},{2,3,1,4},{2,3,4,1},{2,4,1,3},{2,4,3,1},
    {3,1,2,4},{3,1,4,2},{3,2,1,4},{3,2,4,1},{3,4,1,2},{3,4,2,1},
    {4,1,2,3},{4,1,3,2},{4,2,1,3},{4,2,3,1},{4,3,1,2},{4,3,2,1}
}

local function decode(base)
    local pid   = r32(base + 0x00)
    local otid  = r32(base + 0x04)
    local key   = pid ~ otid
    local order = orders[(pid % 24) + 1]

    -- Raw blocks desencriptados
    local block = {}
    for i = 0, 11 do
        block[i+1] = r32(base + 0x20 + i*4) ~ key
    end

    -- Asignar subgrupos G=1 A=2 E=3 M=4
    local g = {}
    for i = 1, 4 do
        local start = (i-1)*3 + 1
        g[order[i]] = { block[start], block[start+1], block[start+2] }
    end

    -- Growth (G=1): species, item, exp, pp_bonuses, friendship
    local species    = g[1][1] & 0xFFFF
    local item_held  = (g[1][1] >> 16) & 0xFFFF
    local exp        = g[1][2]
    local pp_bonuses = g[1][3] & 0xFF
    local friendship = (g[1][3] >> 8) & 0xFF

    -- Attacks (A=2): move1-4, pp1-4
    local move1 = g[2][1] & 0xFFFF
    local move2 = (g[2][1] >> 16) & 0xFFFF
    local move3 = g[2][2] & 0xFFFF
    local move4 = (g[2][2] >> 16) & 0xFFFF
    local pp1   = g[2][3] & 0xFF
    local pp2   = (g[2][3] >> 8) & 0xFF
    local pp3   = (g[2][3] >> 16) & 0xFF
    local pp4   = (g[2][3] >> 24) & 0xFF

    -- EVs & Condition (E=3)
    local ev_hp    = g[3][1] & 0xFF
    local ev_atk   = (g[3][1] >> 8) & 0xFF
    local ev_def   = (g[3][1] >> 16) & 0xFF
    local ev_spe   = (g[3][1] >> 24) & 0xFF
    local ev_spatk = g[3][2] & 0xFF
    local ev_spdef = (g[3][2] >> 8) & 0xFF

    -- Misc (M=4): IVs, egg flag, ability
    local iv_word  = g[4][2]
    local iv_hp    = iv_word & 0x1F
    local iv_atk   = (iv_word >> 5) & 0x1F
    local iv_def   = (iv_word >> 10) & 0x1F
    local iv_spe   = (iv_word >> 15) & 0x1F
    local iv_spatk = (iv_word >> 20) & 0x1F
    local iv_spdef = (iv_word >> 25) & 0x1F
    local is_egg   = (iv_word >> 30) & 0x1
    local ability  = (iv_word >> 31) & 0x1

    -- Header sin encriptar
    local level  = r8(base + 0x54)
    local hp     = r16(base + 0x56)
    local maxhp  = r16(base + 0x58)
    local status = r32(base + 0x50)

    -- Checksum
    local chk_stored = r16(base + 0x1C)
    local chk_calc = 0
    for _, v in ipairs(block) do
        chk_calc = chk_calc + (v & 0xFFFF) + ((v >> 16) & 0xFFFF)
    end
    chk_calc = chk_calc & 0xFFFF

    -- Shiny
    local tid = otid & 0xFFFF
    local sid = (otid >> 16) & 0xFFFF
    local sv  = (tid ~ sid ~ (pid & 0xFFFF) ~ (pid >> 16)) & 0xFFFF

    console:log("==============================")
    console:log(string.format("PID:      0x%08X", pid))
    console:log(string.format("OTID:     0x%08X  TID:%d SID:%d", otid, tid, sid))
    console:log(string.format("Checksum: stored=%d calc=%d match=%s", chk_stored, chk_calc, tostring(chk_stored==chk_calc)))
    console:log(string.format("Shiny:    SV=%d -> %s", sv, tostring(sv < 8)))
    console:log("--- Growth ---")
    console:log(string.format("Species:  %d (0x%04X)", species, species))
    console:log(string.format("Item:     %d", item_held))
    console:log(string.format("Exp:      %d", exp))
    console:log(string.format("PP bonus: %d  Friendship: %d", pp_bonuses, friendship))
    console:log("--- Attacks ---")
    console:log(string.format("Moves:    %d %d %d %d", move1, move2, move3, move4))
    console:log(string.format("PP:       %d %d %d %d", pp1, pp2, pp3, pp4))
    console:log("--- EVs ---")
    console:log(string.format("HP:%d ATK:%d DEF:%d SPE:%d SPATK:%d SPDEF:%d", ev_hp, ev_atk, ev_def, ev_spe, ev_spatk, ev_spdef))
    console:log("--- IVs ---")
    console:log(string.format("HP:%d ATK:%d DEF:%d SPE:%d SPATK:%d SPDEF:%d", iv_hp, iv_atk, iv_def, iv_spe, iv_spatk, iv_spdef))
    console:log(string.format("Egg:%d Ability:%d", is_egg, ability))
    console:log("--- Battle ---")
    console:log(string.format("Level:%d  HP:%d/%d  Status:%d", level, hp, maxhp, status))
end

callbacks:add("frame", function()
    decode(0x030045C0)
end)