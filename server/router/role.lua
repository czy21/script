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

for _, uc_v in ipairs(envJson.param_uci_config) do
    if not uc_v.type
    then
        print("type is empty")
        break
    end
    if command == "backup"
    then
        uci:foreach(envJson.param_role_name, uc_v.type, function(s)
            if uc_v.section
            then
                if s[".name"] == uc_v.section or string.match(s[".name"], uc_v.section)
                then
                    obj[s[".name"]] = s
                end
            else
                obj[uc_v.type] = not obj[uc_v.type] and {} or obj[uc_v.type]
                if not s["name"] or s[".name"] ~= s["name"] then
                    table.insert(obj[uc_v.type], s)
                end
            end
            for k in pairs(s) do
                if string.match(k, "^%.") then
                    s[k] = nil
                end
            end
        end)
    elseif command == "restore"
    then
        config_json_content = fs.readfile(config_json)
        if config_json_content == nil then
            print(config_json .. " not exist")
            return
        end
        obj = json.parse(config_json_content)
        uci:delete_all(envJson.param_role_name, uc_v.type, function(s)
            if uc_v.section
            then
                return s[".name"] == uc_v.section or string.match(s[".name"], uc_v.section)
            end
            return not s["name"] or s[".name"] ~= s["name"]
        end)
        for obj_k, obj_v in pairs(obj) do
            if uc_v.section and (obj_k == uc_v.section or string.match(obj_k, uc_v.section))
            then
                uci:section(envJson.param_role_name, uc_v.type, obj_k, {})
                set_option_value(obj_k, obj_v)
            elseif obj_k == uc_v.type and not uc_v.section
            then
                for _, tv in ipairs(obj_v) do
                    section = uci:add(envJson.param_role_name, uc_v.type)
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