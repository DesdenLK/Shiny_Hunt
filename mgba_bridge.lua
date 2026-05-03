local PORT = 8888

local function portInUse(port)
    local probe = socket.connect("127.0.0.1", port)
    if probe ~= nil then
        return true
    end
    return false
end

while portInUse(PORT) do
    PORT = PORT + 1
    if PORT > 8900 then
        console:error("No se encontro puerto libre en el rango 8888-8900")
        return
    end
end

local server = socket.bind("127.0.0.1", PORT)
server:listen()
console:log("Listening on port " .. PORT)

local KEY_MAP = {
    A=1, B=2, SELECT=4, START=8, RIGHT=16, LEFT=32, UP=64, DOWN=128, R=256, L=512
}

local keyQueue = {}  -- each entry: {key=val, sock=sock}
local currentKey = nil
local currentSock = nil
local framesToHold = 60
local frameCount = 0

local framesToAdvance = 0
local advanceSock = nil

callbacks:add("frame", function()
    if currentKey then
        frameCount = frameCount + 1
        if frameCount >= framesToHold then
            emu:clearKeys(currentKey)
            currentKey = nil
            frameCount = 0
            if currentSock then
                currentSock:send("OK\n")
                currentSock = nil
            end
        end
    elseif #keyQueue > 0 then
        local item = table.remove(keyQueue, 1)
        currentKey = item.key
        currentSock = item.sock
        emu:addKeys(currentKey)
        frameCount = 0
    end

    if framesToAdvance > 0 then
        framesToAdvance = framesToAdvance - 1
        if framesToAdvance == 0 and advanceSock then
            advanceSock:send("OK\n")
            advanceSock = nil
        end
    end
end)

local function handleClient(sock)
    sock:add("received", function()
        local data, err = sock:receive(64)
        if data then
            local cmd, addr_str = data:match("^(R%d+):(%x+)")
            if cmd and addr_str then
                local addr = tonumber(addr_str, 16)
                local value = 0
                if cmd == "R32" then
                    value = emu:read32(addr)
                elseif cmd == "R16" then
                    value = emu:read16(addr)
                else
                    value = emu:read8(addr)
                end
                sock:send(tostring(value) .. "\n")

            elseif data:match("^K:%a+") then
                local key_name = data:match("^K:(%a+)")
                local key_val = KEY_MAP[key_name]
                if key_val then
                    table.insert(keyQueue, {key=key_val, sock=sock})
                else
                    sock:send("OK\n")
                end

            elseif data:match("^LS:%d+") then
                local slot = tonumber(data:match("^LS:(%d+)"))
                emu:loadStateSlot(slot)
                sock:send("OK\n")

            elseif data:match("^SR") then
                -- A(1) + B(2) + SELECT(4) + START(8) = 15
                table.insert(keyQueue, {key=15, sock=sock})

            elseif data:match("^AF:%d+") then
                local n = tonumber(data:match("^AF:(%d+)"))
                framesToAdvance = n
                advanceSock = sock
            end
        end
    end)
end

server:add("received", function()
    local client, err = server:accept()
    if client then
        handleClient(client)
    end
end)
