local string = string
local tostring = tostring
local io = io
local table = table
local pairs = pairs
local open     = io.open
local tonumber = tonumber
local os = os
local math = math
local awful = require("awful")
local naughty = require("naughty")
local beautiful = require('beautiful')
module("bathoover")

local popup

local bathoover = {}

function bathoover:addToWidget(print,mywidget)
        mywidget:connect_signal('mouse::enter', function ()
        status = "N/A"
        capacity = "N/A"
        full_capacity = "N/A"
        charge_now = "N/A"
        charge_full_design = "N/A"
        charge_full = "N/A"
        voltage_now = "N/A"
        current_now = "N/A"
        info = ""
        timeleft = 0
        timeleftAvg = 0
        timeleft100 = 0
        timeleft1000 = 0
        avgCons = 0
        local f = open("/sys/class/power_supply/BAT0/uevent")
        if f then
            while true do
                line = f:read()
                if line == nil then break end
                i,j = string.find(line,"=")
                if string.find(line,"Y_NAME") then
                    info = string.sub(line,j+1) .. info
                end
                if string.find(line,"TECHN") then
                    info = info .. " - " .. string.sub(line,j+1) .. " -"
                end
                if string.find(line,"MODEL_NAME") then
                    info = info .. " " .. string.sub(line,j+1)
                end
                if string.find(line,"MANUF") then
                    info = info .. " " .. string.sub(line,j+1)
                end
                if string.find(line,"NUMBER") then
                    info = info .. " " .. string.sub(line,j+1)
                end
                if string.find(line,"STATUS") then
                    status = string.sub(line,j+1)
                end
                if string.find(line,"CAPACITY=") then
                    capacity = string.sub(line,j+1)
                end
                if string.find(line,"CHARGE_NOW") then
                    charge_now = string.sub(line,j+1)/1000.
                end
                if string.find(line,"CHARGE_FULL") then
                    charge_full = string.sub(line,j+1)/1000.  
                end
                if string.find(line,"CHARGE_FULL_DESIGN") then
                    charge_full_design = string.sub(line,j+1)/1000. 
                end
                if string.find(line,"VOLTAGE_NOW") then
                    voltage_now = string.sub(line,j+1)/1000.
                end
                if string.find(line,"CURRENT_NOW") then
                    current_now = string.sub(line,j+1)/1000.
                end
            end
            f:close()
        end
        os.execute("cp -f  /home/potterat/.config/awesome/powercons.txt /home/potterat/.config/awesome/powercons.tmp.txt") 
        f0 = open("/home/potterat/.config/awesome/powercons.tmp.txt")
        if f0 then
            local n=0
            local n100=0
            local n1000=0
            local t100 = 60
            local t1000 = 450
            while true do
                line = f0:read()
                if line == nil then break end
                timeleftAvg = timeleftAvg+tonumber(line)/1000.
                n=n+1
            end
            timeleftAvg = timeleftAvg/n
            f0:close()
            if n<t1000 then
                timeleft1000 = timeleftAvg
            else 
                n1000 = n - t1000
                ntmp = 0
                ntmp2 = 0
                f0 = open("/home/potterat/.config/awesome/powercons.tmp.txt")
                while true do
                    line = f0:read()
                    if line == nil then break end
                    if ntmp >=n1000 then
                        timeleft1000 = timeleft1000+tonumber(line)/1000.
                        ntmp2 = ntmp2 +1
                    end
                     ntmp = ntmp+1
                end
                f0:close()
                timeleft1000 = timeleft1000/ntmp2
            end
            if n<t100 then
                timeleft100 = timeleftAvg
            else 
                n100 = n - t100
                ntmp = 0
                ntmp2 = 0
                f0 = open("/home/potterat/.config/awesome/powercons.tmp.txt")
                while true do
                    line = f0:read()
                    if line == nil then break end
                    if ntmp >= n100 then
                        timeleft100 = timeleft100+tonumber(line)/1000.
                        ntmp2 = ntmp2 +1
                    end
                    ntmp=ntmp+1
                end
                f0:close()
                timeleft100 = timeleft100/ntmp2
            end
        end

        if current_now ~= 0 then
            timeleft100 = charge_now/timeleft100
            timeh100 = math.floor(timeleft100)
            timem100 = string.format('%02.0f',math.floor((timeleft100-timeh100)*60))
            timesec100 = string.format('%02.0f',math.floor(((timeleft100-timeh100)*60-timem100)*60))
            timeleft100 = string.format(timeh100 ..":".. timem100 ..":".. timesec100)

            timeleft1000 = charge_now/timeleft1000
            timeh1000 = math.floor(timeleft1000)
            timem1000 = string.format('%02.0f',math.floor((timeleft1000-timeh1000)*60))
            timesec1000 = string.format('%02.0f',math.floor(((timeleft1000-timeh1000)*60-timem1000)*60))
            timeleft1000 = string.format(timeh1000 ..":".. timem1000 ..":".. timesec1000)


            timeleftAvg = charge_now/timeleftAvg
            timehavg = math.floor(timeleftAvg)
            timemavg = string.format('%02.0f',math.floor((timeleftAvg-timehavg)*60))
            timesecavg = string.format('%02.0f',math.floor(((timeleftAvg-timehavg)*60-timemavg)*60))
            timeleftAvg = string.format(timehavg ..":".. timemavg ..":".. timesecavg)

            timeleft = charge_now/current_now
            timeh = math.floor(timeleft)
            timem = string.format('%02.0f',math.floor((timeleft-timeh)*60))
            timesec = string.format('%02.0f',math.floor(((timeleft-timeh)*60-timem)*60))
            timeleft = string.format(timeh ..":".. timem ..":".. timesec)
        end

        if charge_full_design ~= 0 then
            full_capacity = string.format('%3.2f',100*charge_full/charge_full_design)
        end


    local font          = "mono 9"
        popup = naughty.notify({

text =      "<span font_desc=\""..font.."\">"..
                "┌["..info.."]\n"..
                "├status:\t\t"..status.."\n"..
                "├time_left_avg:\t\t"..timeleftAvg.. "\n" ..
                "├time_left_15min:\t"..timeleft1000.. "\n" ..
                "├time_left_2min:\t"..timeleft100.. "\n" ..
                "├time_left_ins:\t\t"..timeleft.. "\n" ..
                "├capacity:\t\t"..capacity.." %\n"..
                "├charge_now:\t\t"..charge_now.." mAh\n"..
                "├charge_full/design:\t"..charge_full.."/" ..charge_full_design.." mAh\n"..
                "| \t\t\t"..full_capacity.." %\n"..
                "├voltage_now:\t\t"..voltage_now.." mV\n"..
                "└current_now:\t\t"..current_now.." mA</span>",
            timeout = 0,
            hover_timeout = 0.5,
            screen = awful.screen.focused()
        })
    end)
    mywidget:connect_signal('mouse::leave', function () naughty.destroy(popup) end)
end


return bathoover


