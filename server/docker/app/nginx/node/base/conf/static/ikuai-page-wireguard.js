webpackJsonp([33], {
    1032: function(e, t, a) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        }),
        t.default = {
            props: ["data"],
            data: function() {
                return {
                    oemSign: 2
                }
            },
            created: function() {
                var e = this;
                window.getHeaders(function() {
                    e.oemSign = window.headers.oemSign
                })
            },
            methods: {}
        }
    },
    1043: function(e, t, a) {
        var i = a(23)(a(1032), a(1044), null, null);
        e.exports = i.exports
    },
    1044: function(e, t) {
        e.exports = {
            render: function() {
                var e = this
                  , t = e.$createElement
                  , a = e._self._c || t;
                return 1 == e.oemSign ? a("div", [a("div", {
                    staticClass: "readme"
                }, [a("span", {
                    staticClass: "note"
                }, [e._v(e._s(e.$t("vpn_ad.help_tip")) + "：")]), e._v(" "), a("div", [e._v(e._s(e.$t("vpn_ad.tip1")))]), e._v(" "), a("div", [e._v(e._s(e.$t("vpn_ad.tip2")))]), e._v(" "), a("div", [e._v(e._s(e.$t("vpn_ad.tip3")))]), e._v(" "), a("div", [e._v(e._s(e.$t("vpn_ad.tip4")))]), e._v(" "), a("div", {
                    domProps: {
                        innerHTML: e._s(e.$t("vpn_ad.tip5"))
                    }
                })])]) : e._e()
            },
            staticRenderFns: []
        }
    },
    1091: function(e, t, a) {
        e.exports = {
            default: a(1150),
            __esModule: !0
        }
    },
    1150: function(e, t, a) {
        a(134),
        a(1154),
        e.exports = a(18).Array.from
    },
    1152: function(e, t, a) {
        "use strict";
        var i = a(36)
          , r = a(104);
        e.exports = function(e, t, a) {
            t in e ? i.f(e, t, r(0, a)) : e[t] = a
        }
    },
    1154: function(e, t, a) {
        "use strict";
        var i = a(54)
          , r = a(32)
          , s = a(138)
          , l = a(364)
          , n = a(363)
          , o = a(141)
          , d = a(1152)
          , p = a(356);
        r(r.S + r.F * !a(365)(function(e) {
            Array.from(e)
        }), "Array", {
            from: function(e) {
                var t, a, r, c, u = s(e), v = "function" == typeof this ? this : Array, _ = arguments.length, m = _ > 1 ? arguments[1] : void 0, b = void 0 !== m, f = 0, h = p(u);
                if (b && (m = i(m, _ > 2 ? arguments[2] : void 0, 2)),
                void 0 == h || v == Array && n(h))
                    for (t = o(u.length),
                    a = new v(t); t > f; f++)
                        d(a, f, b ? m(u[f], f) : u[f]);
                else
                    for (c = h.call(u),
                    a = new v; !(r = c.next()).done; f++)
                        d(a, f, b ? l(c, m, [r.value, f], !0) : r.value);
                return a.length = f,
                a
            }
        })
    },
    1519: function(e, t, a) {
        "use strict";
        t.__esModule = !0;
        var i = a(349)
          , r = function(e) {
            return e && e.__esModule ? e : {
                default: e
            }
        }(i);
        t.default = r.default || function(e) {
            for (var t = 1; t < arguments.length; t++) {
                var a = arguments[t];
                for (var i in a)
                    Object.prototype.hasOwnProperty.call(a, i) && (e[i] = a[i])
            }
            return e
        }
    },
    1520: function(e, t, a) {
        "use strict";
        t.__esModule = !0;
        var i = a(1091)
          , r = function(e) {
            return e && e.__esModule ? e : {
                default: e
            }
        }(i);
        t.default = function(e) {
            if (Array.isArray(e)) {
                for (var t = 0, a = Array(e.length); t < e.length; t++)
                    a[t] = e[t];
                return a
            }
            return (0,
            r.default)(e)
        }
    },
    1743: function(e, t, a) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var i = a(359)
          , r = a.n(i)
          , s = a(1520)
          , l = a.n(s)
          , n = a(80)
          , o = a.n(n)
          , d = a(1519)
          , p = a.n(d)
          , c = a(78)
          , u = a(79)
          , v = a.n(u)
          , _ = a(1043)
          , m = a.n(_);
        t.default = {
            components: {
                VpnAdPartial: m.a
            },
            data: function() {
                var e = this;
                return {
                    PWDis_show: !1,
                    shouHint: !1,
                    tableOptions: {
                        clickToEdit: !1,
                        rowEditFormat: "tableForm",
                        tableClass: "table table_w checkbox_checked",
                        customMethods: {},
                        pagination: {
                            paginateable: !0
                        },
                        tableOperation: [{
                            type: "addRow",
                            disable: !1
                        }, {
                            type: "importFile",
                            disable: !1
                        }, {
                            type: "exportFile",
                            disable: !1
                        }, {
                            type: "batchEnableRows",
                            disable: !1
                        }, {
                            type: "batchDisableRows",
                            disable: !1
                        }, {
                            type: "batchDeleteRows",
                            disable: !1
                        }, {
                            type: "reorderRows",
                            disable: !1
                        }, {
                            type: "autoRefresh",
                            disable: !1
                        }],
                        requests: {
                            param: {
                                TYPE: "total,data"
                            },
                            url: c.a.apiUrl,
                            funcName: "wireguard",
                            listAction: "show",
                            delRowAction: "del",
                            enableRowAction: "up",
                            disableRowAction: "down",
                            addRowAction: "add",
                            editRowAction: "edit"
                        },
                        fixColumns: ["id", "buttons", "checkbox", "enabled"],
                        columns: [{
                            name: "name",
                            display: "text",
                            headerLabel: "wire_guard.name",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "local_address",
                            display: "text",
                            headerLabel: "wire_guard.localIP",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "interface",
                            display: "customFunction",
                            headerLabel: "wire_guard.Circuit",
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: "",
                            dataFunction: function(t) {
                                return "auto" === t ? e.$t("vpn.openVpnClient.auto") : t
                            }
                        }, {
                            name: "local_listenport",
                            display: "text",
                            headerLabel: "wire_guard.listeningPort",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "endpoint_port",
                            display: "text",
                            headerLabel: "wire_guard.OppositePort",
                            validate: {
                                reg: "required"
                            },
                            dataLabel: "",
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "upload",
                            display: "customFunction",
                            headerLabel: "wire_guard.upstream",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: "",
                            dataFunction: function(e) {
                                return "" == e ? "" : v.a.formatBytes(e)
                            }
                        }, {
                            name: "download",
                            display: "customFunction",
                            headerLabel: "wire_guard.downloadstream",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: "",
                            dataFunction: function(e) {
                                return "" == e ? "" : v.a.formatBytes(e)
                            }
                        }, {
                            name: "enabled",
                            headerLabel: "wire_guard.Status",
                            display: "customHtmlFunction",
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: "",
                            dataFunction: function(t) {
                                return "yes" === t ? "<span class='colorG'>" + e.$t("common.state_enabled") + "</span>" : "<span class='colorR'>" + e.$t("common.state_disabled") + "</span>"
                            }
                        }, {
                            name: "buttons",
                            headerLabel: "common.operation",
                            display: "buttons",
                            cls: {
                                headerClass: "",
                                cellClass: "td_opear"
                            }
                        }, {
                            name: "checkbox",
                            headerLabel: "",
                            display: "checkbox",
                            cls: {
                                headerClass: "td_check tc tm",
                                cellClass: "tc tm"
                            }
                        }]
                    },
                    tableRowEditing: !1,
                    tableForm: {
                        name: "",
                        local_publickey: "",
                        peer_publickey: "",
                        presharedkey: "",
                        local_address: "10.0.8.1/24",
                        interface: "",
                        keepalive: "",
                        local_listenport: "",
                        local_privatekey: "",
                        allowips: "",
                        endpoint: "",
                        endpoint_port: "",
                        enabled: "yes"
                    },
                    interfaces: [],
                    xEnterprise: 0,
                    oemSign: 0
                }
            },
            created: function() {
                var e = this;
                window.getHeaders(function() {
                    e.xEnterprise = window.headers.xEnterprise,
                    e.oemSign = window.headers.oemSign,
                    1 == e.xEnterprise && e.getInterfaceAndServiceStatus()
                })
            },
            methods: {
                getPrivateKey: function() {
                    var e = this;
                    this.$http.post(this.tableOptions.requests.url, {
                        func_name: "wireguard",
                        action: "show",
                        param: {
                            TYPE: "gen_privatekey"
                        }
                    }).then(function(t) {
                        e.tableForm.local_publickey = t.data.Data.pubkey,
                        e.tableForm.local_privatekey = t.data.Data.privatekey
                    })
                },
                getShareKey: function() {
                    var e = this;
                    this.$http.post(this.tableOptions.requests.url, {
                        func_name: "wireguard",
                        action: "show",
                        param: {
                            TYPE: "gen_sharedkey"
                        }
                    }).then(function(t) {
                        e.tableForm.presharedkey = t.data.Data.presharedkey
                    })
                },
                getInterfaceAndServiceStatus: function() {
                    var e = this;
                    this.$http.post(this.tableOptions.requests.url, {
                        func_name: "wireguard",
                        action: "show",
                        param: {
                            TYPE: "interface"
                        }
                    }).then(function(t) {
                        e.interfaces = copyAry("decode", t.data.Data.interface)
                    })
                },
                saveForm: function() {
                    var e = this;
                    this.$validator.validateAll({
                        name: this.tableForm.name,
                        local_address: this.tableForm.local_address,
                        interface: this.tableForm.interface,
                        local_listenport: this.tableForm.local_listenport,
                        pubkey: this.tableForm.pubkey,
                        local_privatekey: this.tableForm.local_privatekey,
                        peer_publickey: this.tableForm.peer_publickey,
                        keepalive: this.tableForm.keepalive,
                        presharedkey: this.tableForm.presharedkey,
                        allowips: this.tableForm.allowips,
                        endpoint: this.tableForm.endpoint,
                        endpoint_port: this.tableForm.endpoint_port
                    }).then(function(t) {
                        if (!t)
                            return !1;
                        var a = p()({}, JSON.parse(o()(e.tableForm)), {
                            allowips: [].concat(l()(new r.a(e.tableForm.allowips.split("\n")))).join(","),
                            local_listenport: 1 * e.tableForm.local_listenport
                        });
                        e.$http.post(c.a.apiUrl, {
                            func_name: "wireguard",
                            action: e.shouHint ? "edit" : "add",
                            param: copyObj("encode", a)
                        }).then(function(t) {
                            customSuccess(e.$t("common.saveSuccess")),
                            e.tableRowEditing = !1,
                            e.$refs.dtable.reload()
                        })
                    })
                },
                newTableRow: function() {
                    this.tableForm = {
                        name: "wg",
                        local_address: "10.0.8.1/24",
                        interface: "auto",
                        local_listenport: 5e4,
                        local_publickey: "",
                        local_privatekey: "",
                        pubkey: "",
                        peer_publickey: "",
                        keepalive: 10,
                        presharedkey: "",
                        allowips: "",
                        endpoint_port: "",
                        endpoint: "",
                        enabled: "yes"
                    },
                    this.shouHint = !1,
                    this.tableRowEditing = !0,
                    this.getPrivateKey()
                },
                editTableRow: function(e) {
                    this.tableForm = p()({}, JSON.parse(o()(e)), {
                        allowips: e.allowips.replace(/,/g, "\n")
                    }),
                    this.shouHint = !0,
                    this.tableRowEditing = !0
                }
            }
        }
    },
    1865: function(e, t, a) {
        t = e.exports = a(756)(),
        t.push([e.i, "", ""])
    },
    2030: function(e, t, a) {
        var i = a(1865);
        "string" == typeof i && (i = [[e.i, i, ""]]),
        i.locals && (e.exports = i.locals);
        a(757)("096bbe76", i, !0)
    },
    2266: function(e, t) {
        e.exports = {
            render: function() {
                var e = this
                  , t = e.$createElement
                  , a = e._self._c || t;
                return a("div", {
                    staticClass: "qaq3"
                }, [1 ? a("div", [a("div", {
                    directives: [{
                        name: "show",
                        rawName: "v-show",
                        value: !e.tableRowEditing,
                        expression: "!tableRowEditing"
                    }],
                    staticClass: "main_section"
                }, [a("sub-title-section", {
                    attrs: {
                        opturl: {
                            helpUrl: "id=1264&Itemid=1897"
                        },
                        opt: {
                            helpMessage: e.$t("helpTip.wireguardTip")
                        }
                    }
                }), e._v(" "), a("div", {
                    staticClass: "wrapper row"
                }, [a("div", {
                    staticClass: "box clearfix"
                }, [a("d-table", {
                    ref: "dtable",
                    attrs: {
                        opt: e.tableOptions
                    },
                    on: {
                        editTableRow: e.editTableRow,
                        newTableRow: e.newTableRow,
                        tableLoaded: function(t) {
                            e.globalBus.$emit("loadComplete")
                        }
                    }
                }), e._v(" "), a("vpn-ad-partial")], 1)])], 1), e._v(" "), e.tableRowEditing ? a("div", {
                    staticClass: "main_section_edit"
                }, [a("div", {
                    staticClass: "title_h3"
                }, [a("h3", [e._v(e._s(e.tableForm.id ? e.$t("common.edit") : e.$t("common.add")))]), e._v(" "), a("div", {
                    staticClass: "helpService"
                }, [a("a", {
                    staticClass: "close_edit close_ico",
                    attrs: {
                        href: "javascript:void(0)"
                    },
                    on: {
                        click: function(t) {
                            e.tableRowEditing = !1
                        }
                    }
                }, [e._v("×")])])]), e._v(" "), a("div", {
                    staticClass: "wrapper clearfix row"
                }, [a("div", {
                    staticClass: "box"
                }, [a("form", {
                    on: {
                        submit: function(t) {
                            t.preventDefault(),
                            e.saveForm(t)
                        }
                    }
                }, [a("div", {
                    staticClass: "box_block"
                }, [a("div", {
                    staticClass: "clearfix margin_phone col-lg-11 col-lg-offset-1 "
                }, [a("div", {
                    staticClass: "h40"
                }), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.name")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.name,
                        expression: "tableForm.name"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|wireguardName",
                        expression: "'required|wireguardName'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "name",
                        type: "text",
                        placeholder: "wg",
                        "data-vv-as": e.$t("wire_guard.name")
                    },
                    domProps: {
                        value: e.tableForm.name
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.name = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("name") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("name")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.localIP")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.local_address,
                        expression: "tableForm.local_address"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|IPMask",
                        expression: "'required|IPMask'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "local_address",
                        type: "text",
                        "data-vv-as": e.$t("wire_guard.localIP")
                    },
                    domProps: {
                        value: e.tableForm.local_address
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.local_address = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [a("span", {
                    staticClass: "remark margin-l-10"
                }, [e._v("\n                                            " + e._s(e.$t("behavior.table_header_title.reaction")) + "\n                                        ")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("local_address") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("local_address")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.listeningPort")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.local_listenport,
                        expression: "tableForm.local_listenport"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|numeric|between:10,65535",
                        expression: "'required|numeric|between:10,65535'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "listeningPort",
                        type: "text",
                        "data-vv-as": e.$t("wire_guard.listeningPort")
                    },
                    domProps: {
                        value: e.tableForm.local_listenport
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.local_listenport = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("listeningPort") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v("\n                                            " + e._s(e.errors.first("listeningPort")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.localpublicKey")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.local_publickey,
                        expression: "tableForm.local_publickey"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|filterSpecialChar2",
                        expression: "'required|filterSpecialChar2'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "localpublicKey",
                        "data-vv-as": e.$t("wire_guard.localpublicKey"),
                        type: "text",
                        autocomplete: "off",
                        readonly: ""
                    },
                    domProps: {
                        value: e.tableForm.local_publickey
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.local_publickey = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")]), e._v(" "), a("a", {
                    staticClass: "btn btn_blue btn_confirm",
                    on: {
                        click: function(t) {
                            e.getPrivateKey()
                        }
                    }
                }, [e._v(e._s(e.$t("wire_guard.generateLocalKey")))])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("localpublicKey") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("localpublicKey")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.privatekey")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.local_privatekey,
                        expression: "tableForm.local_privatekey"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|filterSpecialChar2",
                        expression: "'required|filterSpecialChar2'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "local_privatekey",
                        "data-vv-as": e.$t("wire_guard.privatekey"),
                        type: "text",
                        autocomplete: "off",
                        readonly: ""
                    },
                    domProps: {
                        value: e.tableForm.local_privatekey
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.local_privatekey = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("local_privatekey") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("local_privatekey")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.peerpublicKey")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "validate",
                        rawName: "v-validate",
                        value: "required",
                        expression: "'required'"
                    }, {
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.peer_publickey,
                        expression: "tableForm.peer_publickey"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "peer_publickey",
                        "data-vv-as": e.$t("wire_guard.peerpublicKey"),
                        type: "text"
                    },
                    domProps: {
                        value: e.tableForm.peer_publickey
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.peer_publickey = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("peer_publickey") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("peer_publickey")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.oppositeIP")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.endpoint,
                        expression: "tableForm.endpoint"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "ipordomain2",
                        expression: "'ipordomain2'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "endpoint",
                        "data-vv-as": e.$t("wire_guard.oppositeIP"),
                        type: "text",
                        autocomplete: "off"
                    },
                    domProps: {
                        value: e.tableForm.endpoint
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.endpoint = t.target.value)
                        }
                    }
                })]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("endpoint") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("endpoint")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.oppositePort")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.endpoint_port,
                        expression: "tableForm.endpoint_port"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "numeric|between:10,65535",
                        expression: "'numeric|between:10,65535'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "endpoint_port",
                        type: "text",
                        "data-vv-as": e.$t("wire_guard.oppositePort"),
                        autocomplete: "off"
                    },
                    domProps: {
                        value: e.tableForm.endpoint_port
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.endpoint_port = t.target.value)
                        }
                    }
                })]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("endpoint_port") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("endpoint_port")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.heartbeatInterval")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.keepalive,
                        expression: "tableForm.keepalive"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|numeric|between:0,500",
                        expression: "'required|numeric|between:0,500'"
                    }],
                    staticClass: "inptText w120",
                    attrs: {
                        name: "heartbeatInterval",
                        type: "text",
                        "data-vv-as": e.$t("wire_guard.heartbeatInterval")
                    },
                    domProps: {
                        value: e.tableForm.keepalive
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.keepalive = t.target.value)
                        }
                    }
                }), e._v("\n                                        " + e._s(e.$t("common.second")) + "\n                                        "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [a("span", {
                    staticClass: "remark margin-l-10"
                }, [e._v("\n                                            " + e._s(e.$t("behavior.table_header_title.head_pool")) + "\n                                        ")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("heartbeatInterval") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("heartbeatInterval")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.preSharedKey")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.presharedkey,
                        expression: "tableForm.presharedkey"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "filterSpecialChar2|strLenBetween:1,64",
                        expression: "'filterSpecialChar2|strLenBetween:1,64'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "preSharedKey",
                        type: "text",
                        "data-vv-as": e.$t("wire_guard.preSharedKey"),
                        autocomplete: "off"
                    },
                    domProps: {
                        value: e.tableForm.presharedkey
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.presharedkey = t.target.value)
                        }
                    }
                })]), e._v(" "), a("a", {
                    staticClass: "btn btn_blue btn_confirm",
                    on: {
                        click: function(t) {
                            e.getShareKey()
                        }
                    }
                }, [e._v(e._s(e.$t("wire_guard.generateSharedKey")))]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("preSharedKey") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("preSharedKey")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.Circuit")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("div", {
                    staticClass: "search_list"
                }, [a("select", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.interface,
                        expression: "tableForm.interface"
                    }],
                    staticClass: "selects",
                    attrs: {
                        name: "interface"
                    },
                    on: {
                        change: function(t) {
                            var a = Array.prototype.filter.call(t.target.options, function(e) {
                                return e.selected
                            }).map(function(e) {
                                return "_value"in e ? e._value : e.value
                            });
                            e.tableForm.interface = t.target.multiple ? a : a[0]
                        }
                    }
                }, [a("option", {
                    attrs: {
                        value: "auto"
                    }
                }, [e._v(e._s(e.$t("vpn.openVpnClient.auto")))]), e._v(" "), e._l(e.interfaces, function(t) {
                    return a("option", {
                        domProps: {
                            value: t[0]
                        }
                    }, [e._v("\n                                                    " + e._s(t[0] + (t.length > 1 ? "(" + t[1] + ")" : "")) + "\n                                                ")])
                })], 2)])])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("wire_guard.allowTargetnetworkSegments")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("textarea", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.allowips,
                        expression: "tableForm.allowips"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|ipOrMaskList",
                        expression: "'required|ipOrMaskList'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "allowips",
                        rows: "",
                        "data-vv-as": e.$t("wire_guard.allowTargetnetworkSegments"),
                        placeholder: e.$t("vpn.openVpnClient.route_format")
                    },
                    domProps: {
                        value: e.tableForm.allowips
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.allowips = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("allowips") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("allowips")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "h20"
                }), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_group"
                }, [a("button", {
                    staticClass: "btn btn_green btn_confirm",
                    attrs: {
                        type: "submit",
                        name: "button"
                    }
                }, [e._v("\n                                            " + e._s(e.$t("common.save")) + "\n                                        ")]), e._v(" "), a("button", {
                    staticClass: "btn btn_cancel margin-l-10",
                    attrs: {
                        type: "button"
                    },
                    on: {
                        click: function(t) {
                            e.tableRowEditing = !1
                        }
                    }
                }, [e._v("\n                                            " + e._s(e.$t("common.cancel")) + "\n                                        ")])])])])])])])])]) : e._e()]) : a("div", {
                    staticClass: "main_section"
                }, [a("sub-title-section", {
                    attrs: {
                        opturl: {
                            helpUrl: "id=1264&Itemid=1897"
                        },
                        opt: {
                            helpMessage: e.$t("helpTip.wireguardTip")
                        }
                    }
                }), e._v(" "), a("div", {
                    staticStyle: {
                        width: "100%",
                        "text-align": "center",
                        "line-height": "150%",
                        "margin-top": "20%",
                        "font-size": "14px"
                    }
                }, [a("i", {
                    staticClass: "ico-mark"
                }), e._v(e._s(e.$t("common.xEnterprise_2")) + "\n        ")])], 1)])
            },
            staticRenderFns: []
        }
    },
    929: function(e, t, a) {
        a(2030);
        var i = a(23)(a(1743), a(2266), "data-v-6a1474b8", null);
        e.exports = i.exports
    }
});
