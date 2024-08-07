webpackJsonp([61], {
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
        var s = a(23)(a(1032), a(1044), null, null);
        e.exports = s.exports
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
    1733: function(e, t, a) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var s = a(80)
          , i = a.n(s)
          , r = a(353)
          , n = a.n(r)
          , l = a(78)
          , o = a(79)
          , d = (a.n(o),
        a(1043))
          , c = a.n(d);
        t.default = {
            components: {
                VpnAdPartial: c.a
            },
            data: function() {
                var e, t = this;
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
                            url: l.a.apiUrl,
                            funcName: "ike_client",
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
                            headerLabel: "ipsec_ikev2.name",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "authby",
                            display: "customFunction",
                            headerLabel: "ipsec_ikev2.type",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "table_IPMAC_w",
                                cellClass: "td-no-wrap"
                            },
                            addDefault: "",
                            dataFunction: function(e) {
                                return "mschapv2" == e ? "IKEv2/IPsec MSCHAPv2" : "IKEv2/IPsec PSK"
                            }
                        }, {
                            name: "remote_addr",
                            display: "text",
                            headerLabel: "ipsec_ikev2.remote_addr",
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
                            headerLabel: "ipsec_ikev2.interface",
                            validate: {
                                reg: "required"
                            },
                            dataLabel: "",
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: "",
                            dataFunction: function(e) {
                                return "auto" == e ? t.$t("vpn.l2tpclient.auto") : e
                            }
                        }, {
                            name: "ip_addr",
                            display: "text",
                            headerLabel: "vpn.pptpclient.ip_addr",
                            validate: {
                                reg: "required"
                            },
                            dataLabel: "",
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, (e = {
                            name: "enabled",
                            display: "text",
                            headerLabel: "common.enabled"
                        },
                        n()(e, "display", "enabled"),
                        n()(e, "cls", {
                            headerClass: "",
                            cellClass: ""
                        }),
                        n()(e, "addDefault", ""),
                        e), {
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
                        authby: "mschapv2",
                        name: "iked",
                        username: "",
                        passwd: "",
                        interface: "auto",
                        secret: "",
                        remote_addr: "",
                        leftid: "",
                        rightid: "",
                        enabled: "yes"
                    },
                    interfaces: [],
                    xEnterprise: 0,
                    oemSign: 0
                }
            },
            methods: {
                getInterfaceAndServiceStatus: function() {
                    var e = this;
                    this.$http.post(this.tableOptions.requests.url, {
                        func_name: "ike_client",
                        action: "show",
                        param: {
                            TYPE: "interface"
                        }
                    }).then(function(t) {
                        e.interfaces = copyAry("decode", t.data.Data.interface)
                    })
                },
                typeChange: function() {
                    var e = this
                      , t = this.tableForm.authby;
                    this.tableForm.authby = "",
                    setTimeout(function() {
                        e.tableForm.authby = t
                    }, 15)
                },
                saveForm: function() {
                    var e = this;
                    this.$validator.validateAll({
                        username: this.tableForm.username,
                        passwd: this.tableForm.passwd,
                        name: this.tableForm.name,
                        remote_addr: this.tableForm.remote_addr,
                        secret: this.tableForm.secret,
                        leftid: this.tableForm.leftid,
                        rightid: this.tableForm.rightid
                    }).then(function(t) {
                        if (!t)
                            return !1;
                        e.$http.post(e.tableOptions.requests.url, {
                            func_name: "ike_client",
                            action: e.shouHint ? "edit" : "add",
                            param: copyObj("encode", e.tableForm)
                        }).then(function(t) {
                            customSuccess(e.$t("common.saveSuccess")),
                            e.tableRowEditing = !1,
                            e.$refs.dtable.reload()
                        })
                    })
                },
                newTableRow: function() {
                    this.tableForm = {
                        authby: "mschapv2",
                        name: "iked",
                        username: "",
                        passwd: "",
                        interface: "auto",
                        secret: "",
                        remote_addr: "",
                        leftid: "",
                        rightid: "",
                        enabled: "yes"
                    },
                    this.shouHint = !1,
                    this.tableRowEditing = !0
                },
                editTableRow: function(e) {
                    this.tableForm = JSON.parse(i()(e)),
                    this.shouHint = !0,
                    this.tableRowEditing = !0
                }
            },
            created: function() {
                var e = this;
                window.getHeaders(function() {
                    e.xEnterprise = window.headers.xEnterprise,
                    e.oemSign = window.headers.oemSign,
                    1 == e.xEnterprise && e.getInterfaceAndServiceStatus()
                })
            }
        }
    },
    1905: function(e, t, a) {
        t = e.exports = a(756)(),
        t.push([e.i, "", ""])
    },
    2070: function(e, t, a) {
        var s = a(1905);
        "string" == typeof s && (s = [[e.i, s, ""]]),
        s.locals && (e.exports = s.locals);
        a(757)("f0cab14c", s, !0)
    },
    2310: function(e, t) {
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
                            helpUrl: "id=1079&Itemid=1662"
                        },
                        opt: {
                            helpMessage: e.$t("helpTip.ikev2clientTip")
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
                }, [e._v(e._s(e.$t("ipsec_ikev2.name")) + "：")]), e._v(" "), a("div", {
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
                        value: "required|ikedName|alpha_dash",
                        expression: "'required|ikedName|alpha_dash'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "name",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.name")
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
                }, [e._v(e._s(e.$t("ipsec_ikev2.type")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("select", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.authby,
                        expression: "tableForm.authby"
                    }],
                    staticClass: "selects margin-r-20",
                    on: {
                        change: [function(t) {
                            var a = Array.prototype.filter.call(t.target.options, function(e) {
                                return e.selected
                            }).map(function(e) {
                                return "_value"in e ? e._value : e.value
                            });
                            e.tableForm.authby = t.target.multiple ? a : a[0]
                        }
                        , function(t) {
                            e.typeChange()
                        }
                        ]
                    }
                }, [a("option", {
                    attrs: {
                        value: "mschapv2"
                    }
                }, [e._v("IKEv2/IPsec MSCHAPv2")]), e._v(" "), a("option", {
                    attrs: {
                        value: "secret"
                    }
                }, [e._v("IKEv2/IPsec PSK")])])])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.remote_addr")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.remote_addr,
                        expression: "tableForm.remote_addr"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|ipordomain2",
                        expression: "'required|ipordomain2'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "remote_addr",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.remote_addr")
                    },
                    domProps: {
                        value: e.tableForm.remote_addr
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.remote_addr = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("remote_addr") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v("\n                                            " + e._s(e.errors.first("remote_addr")))]) : e._e()])]), e._v(" "), "mschapv2" == e.tableForm.authby ? a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.username")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.username,
                        expression: "tableForm.username"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|filterSpecialChar2|strLenBetween2:1,64",
                        expression: "'required|filterSpecialChar2|strLenBetween2:1,64'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "username",
                        "data-vv-as": e.$t("ipsec_ikev2.username"),
                        type: "text",
                        autocomplete: "off"
                    },
                    domProps: {
                        value: e.tableForm.username
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.username = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("username") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("username")))]) : e._e()])]) : e._e(), e._v(" "), "mschapv2" == e.tableForm.authby ? a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.passwd")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("div", {
                    staticClass: "show_password",
                    staticStyle: {
                        display: "inline-block"
                    }
                }, [a("a", {
                    staticClass: "eyes open_eye",
                    class: e.PWDis_show ? "close_eye" : "open_eye",
                    attrs: {
                        type: "button"
                    },
                    on: {
                        click: function(t) {
                            e.PWDis_show = !e.PWDis_show
                        }
                    }
                }), e._v(" "), e._m(0), e._v(" "), e.PWDis_show ? e._e() : a("input", {
                    directives: [{
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|filterPassword2|strLenBetween:1,64",
                        expression: "'required|filterPassword2|strLenBetween:1,64'"
                    }, {
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.passwd,
                        expression: "tableForm.passwd"
                    }],
                    staticClass: "inptText password_txt search_inpt",
                    attrs: {
                        name: "passwd",
                        "data-vv-as": e.$t("ipsec_ikev2.passwd"),
                        type: "password",
                        autocomplete: "new-password"
                    },
                    domProps: {
                        value: e.tableForm.passwd
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.passwd = t.target.value)
                        }
                    }
                }), e._v(" "), e.PWDis_show ? a("input", {
                    directives: [{
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|filterPassword2|strLenBetween:1,64",
                        expression: "'required|filterPassword2|strLenBetween:1,64'"
                    }, {
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.passwd,
                        expression: "tableForm.passwd"
                    }],
                    staticClass: "inptText password_txt search_inpt",
                    attrs: {
                        name: "passwd",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.passwd")
                    },
                    domProps: {
                        value: e.tableForm.passwd
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.passwd = t.target.value)
                        }
                    }
                }) : e._e()]), e._v(" "), a("em", {
                    staticStyle: {
                        "margin-left": "10px"
                    }
                }, [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("passwd") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("passwd")) + "\n                                        ")]) : e._e()])]) : e._e(), e._v(" "), "secret" == e.tableForm.authby ? a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.share_secret_key")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|filterSpecialChar2|strLenBetween:1,64",
                        expression: "'required|filterSpecialChar2|strLenBetween:1,64'"
                    }, {
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.secret,
                        expression: "tableForm.secret"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "secret",
                        "data-vv-as": e.$t("ipsec_ikev2.share_secret_key"),
                        type: "text"
                    },
                    domProps: {
                        value: e.tableForm.secret
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.secret = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("secret") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("secret")) + "\n                                        ")]) : e._e()])]) : e._e(), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.local_id")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.leftid,
                        expression: "tableForm.leftid"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|filterSpecialChar2|strLenBetween:1,100",
                        expression: "'required|filterSpecialChar2|strLenBetween:1,100'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "leftid",
                        "data-vv-as": e.$t("ipsec_ikev2.local_id"),
                        type: "text",
                        autocomplete: "off"
                    },
                    domProps: {
                        value: e.tableForm.leftid
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.leftid = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("leftid") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("leftid")) + "\n                                        ")]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.opposite_id")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.rightid,
                        expression: "tableForm.rightid"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "filterSpecialChar2|strLenBetween:1,100",
                        expression: "'filterSpecialChar2|strLenBetween:1,100'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "rightid",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.opposite_id"),
                        autocomplete: "off"
                    },
                    domProps: {
                        value: e.tableForm.rightid
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.rightid = t.target.value)
                        }
                    }
                })]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("rightid") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("rightid")) + "\n                                        ")]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.interface")) + "：")]), e._v(" "), a("div", {
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
                    staticClass: "focuseText selects",
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
                }, e._l(e.interfaces, function(t) {
                    return a("option", {
                        domProps: {
                            value: t[0]
                        }
                    }, [e._v("\n                                                    " + e._s("auto" == t[0] ? e.$t("common.dtable.auto") : t[0] + (t[1] ? "(" + t[1] + ")" : "")) + "\n                                                ")])
                }))])])]), e._v(" "), a("div", {
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
                }, [e._v("\n                                            " + e._s(e.$t("common.save")))]), e._v(" "), a("button", {
                    staticClass: "btn btn_cancel margin-l-10",
                    attrs: {
                        type: "button"
                    },
                    on: {
                        click: function(t) {
                            e.tableRowEditing = !1
                        }
                    }
                }, [e._v(e._s(e.$t("common.cancel")))])])])])])])])])]) : e._e()]) : a("div", {
                    staticClass: "main_section"
                }, [a("sub-title-section", {
                    attrs: {
                        opturl: {
                            helpUrl: "id=1079&Itemid=1662"
                        },
                        opt: {
                            helpMessage: e.$t("helpTip.ikev2clientTip")
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
            staticRenderFns: [function() {
                var e = this
                  , t = e.$createElement
                  , a = e._self._c || t;
                return a("div", {
                    staticStyle: {
                        height: "0",
                        width: "0",
                        overflow: "hidden"
                    }
                }, [a("input", {
                    staticStyle: {
                        visibility: "hidden"
                    }
                }), e._v(" "), a("input", {
                    staticStyle: {
                        visibility: "hidden"
                    },
                    attrs: {
                        type: "password"
                    }
                })])
            }
            ]
        }
    },
    919: function(e, t, a) {
        a(2070);
        var s = a(23)(a(1733), a(2310), "data-v-a63f0816", null);
        e.exports = s.exports
    }
});
