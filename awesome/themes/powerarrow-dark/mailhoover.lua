local string = string
local tostring = tostring
local io = io
local table = table
local pairs = pairs
local os = os
local awful = require("awful")
local json = require("cjson")
local naughty = require("naughty")
local beautiful = require('beautiful')
module("mailhoover")

local popup

local mailhoover = {}

function mailhoover:addToWidget(print,mywidget, querystring, maxcount)
        mywidget:connect_signal('mouse::enter', function ()
local query_format = "<span color='" .. beautiful.fg_urgent .."'><b><u>%s</u>\n</b></span>"
        local info = mailhoover:read_index(print,querystring,maxcount)
        popup = naughty.notify({
            title = "",
            text = string.format(query_format,querystring) .. "<br>" .. info,
            timeout = 0,
            hover_timeout = 0.5,
            screen = awful.screen.focused()
        })
    end)
    mywidget:connect_signal('mouse::leave', function () naughty.destroy(popup) end)
end

function mailhoover:read_index(print,querystring,maxcount)
    local info = ""
    local count = 0

    local f = io.popen("notmuch search --format=json "..querystring)
    local out = f:read("*all")
    print(out)
    f:close()
    local threads = json.decode(out)

    for num,thread in pairs(threads) do
        if count == maxcount then break else count = count +1 end
        date = os.date("%c",thread["timestamp"])
        subject = thread["subject"]
        subject = string.gsub(subject, "&","&")
        subject = string.gsub(subject, "<","<")
        subject = string.gsub(subject, ">",">")
        authors = thread["authors"]
        authors = string.gsub(authors, "<(.*)>","")
        tags = table.concat(thread["tags"],', ')

local thread_format = "<span color='" .. beautiful.fg_normal.."'>%s </span><span color='" .. beautiful.fg_focus .."'>%s </span><span color='" .. beautiful.fg_urgent .."'>(%s)</span>"
        info = info .. string.format(thread_format,date,authors,subject,tags) .. '\n' -- optionally omit timestamps by removing date
    end
    return info
end

return mailhoover


