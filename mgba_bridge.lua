-- mgba_bridge.lua
local socket = require("socket")

local HOST = "127.0.0.1"
local PORT = 8888

local server = socket.bind(HOST, PORT)
server:settimeout(0)

local client = nil

callbacks:add("frame", function()
    if not client then
        local c = server:accept()
        if c then
            c:settimeout(0)
            client = c
        end
    end

    local value = nil

    if client then
        local line, err = client:receive("*l")
        if line then
            local cmd, addr_str = line:match("^(R%d+):(%x+)$")
            local addr = tonumber(addr_str, 16)
            if cmd == "R32" then
                value =  memory.read32(addr)
            elseif cmd == "R16" then
                value =  memory.read16(addr)
            else
                value =  memory.read8(addr)
            end
        client:send(tostring(value) .. "\n")
        elseif err == "closed" then
            client = nil
        end
    end
end)