#!/usr/bin/env lua
local uci = (require "luci.model.uci").cursor()
local json = require "luci.jsonc"
local fs = require "nixio.fs"

local command
local envFile
for i, v in ipairs(arg) do
    if v == "--command"
    then
        command = arg[i + 1]
    end
    if v == "--env-file"
    then
        envFile = arg[i + 1]
    end
end
local envJson = json.parse(fs.readfile(envFile))
if not envJson.param_uci_config
then
    return
end

local config_json = envJson.param_role_temp_path .. "/config.json"
local obj = {}

function set_option_value(section, value)
    for ok, ov in pairs(value) do
        uci:set(envJson.param_role_name, section, ok, ov)
    end
end

for _, uv in ipairs(envJson.param_uci_config) do
    if not uv.type
    then
        print("type is empty")
        break
    end
    if command == "backup"
    then
        role_config = uci:get_all(envJson.param_role_name)
        for ak, av in pairs(role_config == false and {} or role_config) do
            at = av[".type"]
            if at == uv.type or string.match(at, uv.type) then
                if uv.section
                then
                    if ak == uv.section or string.match(ak, uv.section)
                    then
                        obj[ak] = av
                    end
                else
                    obj[at] = not obj[at] and {} or obj[at]
                    if not av["name"] or av[".name"] ~= av["name"] then
                        table.insert(obj[at], av)
                    end
                end
                for k in pairs(av) do
                    if string.match(k, "^%.") then
                        av[k] = nil
                    end
                end
            end
        end
    elseif command == "restore"
    then
        config_json_content = fs.readfile(config_json)
        if config_json_content == nil then
            print(config_json .. " not exist")
            return
        end
        obj = json.parse(config_json_content)
        for ak, av in pairs(uci:get_all(envJson.param_role_name)) do
            at = av[".type"]
            if at == uv.type or string.match(at, uv.type) then
                if uv.section
                then
                    if ak == uv.section or string.match(ak, uv.section) then
                        uci:delete(envJson.param_role_name, ak)
                    end
                else
                    if not av["name"] or av[".name"] ~= av["name"] then
                        uci:delete(envJson.param_role_name, ak)
                    end
                end
            end
        end
        for ck, cv in pairs(obj) do
            if uv.section and (ck == uv.section or string.match(ck, uv.section))
            then
                uci:section(envJson.param_role_name, uv.type, ck, {})
                set_option_value(ck, cv)
            elseif not uv.section and (ck == uv.type or string.match(ck,uv.type))
            then
                for _, tv in ipairs(cv) do
                    section = uci:add(envJson.param_role_name, ck)
                    set_option_value(section, tv)
                end
            end
        end
    end
end
if command == "backup"
then
    fs.writefile(config_json, next(obj) == nil and "{}" or json.stringify(obj, true))
end

if command == "restore"
then
    uci:commit(envJson.param_role_name)
end