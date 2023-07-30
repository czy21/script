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
                if string.match(s[".name"], uc_v.section)
                then
                    obj[s[".name"]] = s
                end
            else
                if not obj[uc_v.type]
                then
                    obj[uc_v.type] = {}
                end
                table.insert(obj[uc_v.type], s)
            end
            for k in pairs(s) do
                if string.match(k, "^%.") then
                    s[k] = nil
                end
            end
        end)
    elseif command == "restore"
    then
        uci:delete_all(envJson.param_role_name, uc_v.type, function(s)
            if uc_v.section
            then
                return string.match(s[".name"], uc_v.section)
            end
            return true
        end)
        obj = json.parse(fs.readfile(config_json))
        for obj_k, obj_v in pairs(obj) do
            if uc_v.section and string.match(obj_k, uc_v.section)
            then
                uci:section(envJson.param_role_name, uc_v.type, obj_k, {})
                for ok, ov in pairs(obj_v) do
                    uci:set(envJson.param_role_name, obj_k, ok, ov)
                end
            elseif obj_k == uc_v.type
            then
                for _, tv in ipairs(obj_v) do
                    section = uci:add(envJson.param_role_name, uc_v.type)
                    for ok, ov in pairs(tv) do
                        uci:set(envJson.param_role_name, section, ok, ov)
                    end
                end
            end
        end
    end
end
if command == "backup"
then
    fs.writefile(config_json, json.stringify(obj, true))
end

if command == "restore"
then
    uci:commit(envJson.param_role_name)
end