webpackJsonp([69], {
    1734: function(e, t, a) {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        });
        var i = a(80)
          , s = a.n(i)
          , r = a(78)
          , l = a(79);
        a.n(l);
        t.default = {
            name: "IKEv2ServerPage",
            components: {},
            data: function() {
                return {
                    tableForm: {
                        enabled: "yes",
                        dns1: "",
                        dns2: "",
                        addrpool: "",
                        leftid: "",
                        rightid: "",
                        secret: "",
                        leftcert: "",
                        privatekey: "",
                        authby: "mschapv2"
                    },
                    newData: {},
                    ischecked: !1,
                    xEnterprise: 0,
                    oemSign: 0
                }
            },
            mounted: function() {
                var e = this;
                window.getHeaders(function() {
                    e.xEnterprise = window.headers.xEnterprise,
                    e.oemSign = window.headers.oemSign,
                    console.log(e.xEnterprise, e.oemSign),
                    1 != e.xEnterprise && 2 != e.oemSign || e.showData()
                })
            },
            methods: {
                saveForm: function() {
                    var e = this;
                    this.$validator.validateAll({
                        addrpool: this.tableForm.addrpool,
                        dns1: this.tableForm.dns1,
                        dns2: this.tableForm.dns2,
                        leftid: this.tableForm.leftid,
                        rightid: this.tableForm.rightid,
                        secret: this.tableForm.secret,
                        leftcert: this.tableForm.leftcert,
                        privatekey: this.tableForm.privatekey
                    }).then(function(t) {
                        if (!t)
                            return !1;
                        var a = JSON.parse(s()(e.tableForm));
                        a.leftcert = a.leftcert.replace(/\n/g, "@").replace(/\s/g, "#"),
                        a.privatekey = a.privatekey.replace(/\n/g, "@").replace(/\s/g, "#"),
                        e.$http.post(r.a.apiUrl, {
                            func_name: "ike_server",
                            action: "save",
                            param: copyObj("encode", a)
                        }).then(function(t) {
                            customSuccess(e.$t("common.saveSuccess"))
                        })
                    })
                },
                showData: function() {
                    var e = this;
                    this.$http.post(r.a.apiUrl, {
                        func_name: "ike_server",
                        action: "show"
                    }).then(function(t) {
                        e.tableForm = t.data.Data.data[0],
                        e.tableForm.leftcert = e.tableForm.leftcert.replace(/@/g, "\n").replace(/#/g, " "),
                        e.tableForm.privatekey = e.tableForm.privatekey.replace(/@/g, "\n").replace(/#/g, " ")
                    })
                },
                changeAuthby: function() {
                    var e = this
                      , t = this.tableForm.authby;
                    this.tableForm.authby = "none",
                    setTimeout(function() {
                        e.tableForm.authby = t
                    }, 20)
                },
                gen_certs: function() {
                    var e = this;
                    this.$validator.validateAll({
                        leftid: this.tableForm.leftid
                    }).then(function(t) {
                        if (!t)
                            return !1;
                        e.$http.post(r.a.apiUrl, {
                            func_name: "ike_server",
                            action: "show",
                            param: {
                                leftid: e.tableForm.leftid,
                                TYPE: "create_certs"
                            }
                        }).then(function(t) {
                            e.tableForm.leftcert = t.data.Data.leftcert,
                            e.tableForm.privatekey = t.data.Data.privatekey
                        })
                    })
                }
            }
        }
    },
    1904: function(e, t, a) {
        t = e.exports = a(756)(),
        t.push([e.i, "", ""])
    },
    2069: function(e, t, a) {
        var i = a(1904);
        "string" == typeof i && (i = [[e.i, i, ""]]),
        i.locals && (e.exports = i.locals);
        a(757)("90f40b5e", i, !0)
    },
    2309: function(e, t) {
        e.exports = {
            render: function() {
                var e = this
                  , t = e.$createElement
                  , a = e._self._c || t;
                return a("div", {
                    staticClass: "qaq3"
                }, [a("sub-title-section", {
                    attrs: {
                        opturl: {
                            helpUrl: "id=1078&Itemid=1661"
                        },
                        opt: {
                            helpMessage: e.$t("helpTip.ikev2serverTip")
                        }
                    }
                }), e._v(" "), 1 ? a("div", [a("div", {
                    staticClass: "wrapper row"
                }, [a("form", {
                    on: {
                        submit: function(t) {
                            t.preventDefault(),
                            e.saveForm(t)
                        }
                    }
                }, [a("div", {
                    staticClass: "box clearfix"
                }, [a("div", {
                    staticClass: "box_block clearfix"
                }, [a("div", {
                    staticClass: "clearfix margin_phone col-lg-11 col-lg-offset-1 "
                }, [a("div", {
                    staticClass: "h40"
                }), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(" " + e._s(e.$t("ipsec_ikev2.status")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("d-switch", {
                    attrs: {
                        opt: {
                            on: "yes",
                            off: "no"
                        }
                    },
                    model: {
                        value: e.tableForm.enabled,
                        callback: function(t) {
                            e.tableForm.enabled = t
                        },
                        expression: "tableForm.enabled"
                    }
                })], 1)]), e._v(" "), a("div", {
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
                            e.changeAuthby()
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
                }, [e._v(e._s(e.$t("ipsec_ikev2.addrpoor")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.addrpool,
                        expression: "tableForm.addrpool"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|IPMask",
                        expression: "'required|IPMask'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "addrpool",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.addrpoor")
                    },
                    domProps: {
                        value: e.tableForm.addrpool
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.addrpool = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("addrpool") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("addrpool")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(" " + e._s(e.$t("ipsec_ikev2.dns1")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.dns1,
                        expression: "tableForm.dns1"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|ip",
                        expression: "'required|ip'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "dns1",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.dns1")
                    },
                    domProps: {
                        value: e.tableForm.dns1
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.dns1 = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("dns1") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("dns1")))]) : e._e()])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(" " + e._s(e.$t("ipsec_ikev2.dns2")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.dns2,
                        expression: "tableForm.dns2"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "required|ip",
                        expression: "'required|ip'"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "dns2",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.dns2")
                    },
                    domProps: {
                        value: e.tableForm.dns2
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.dns2 = t.target.value)
                        }
                    }
                }), e._v(" "), a("em", [e._v("*")])]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("dns2") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("dns2")))]) : e._e()])]), e._v(" "), a("div", {
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
                        value: "required|filterSpecialChar2|strLenBetween:1,64",
                        expression: "'required|filterSpecialChar2|strLenBetween:1,64'"
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
                }, [e._v(e._s(e.errors.first("leftid")))]) : e._e()]), e._v(" "), "mschapv2" == e.tableForm.authby ? a("a", {
                    staticClass: "btn btn_blue height26",
                    attrs: {
                        href: "javascript:void(0);"
                    },
                    on: {
                        click: function(t) {
                            e.gen_certs()
                        }
                    }
                }, [e._v(e._s(e.$t("ipsecvpn.generating_key")))]) : e._e()]), e._v(" "), a("div", {
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
                }, [e._v(e._s(e.errors.first("rightid")))]) : e._e()]), e._v(" "), a("div", {
                    staticClass: "remark"
                }, [a("p", {
                    staticClass: "fl"
                }, [e._v(e._s(e.$t("ipsec_ikev2.opposite_id_tip")))]), a("br")])]), e._v(" "), "secret" == e.tableForm.authby ? a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.share_secret_key")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.secret,
                        expression: "tableForm.secret"
                    }, {
                        name: "validate",
                        rawName: "v-validate",
                        value: "filterSpecialChar2|strLenBetween:1,64",
                        expression: "'filterSpecialChar2|strLenBetween:1,64'"
                    }],
                    staticClass: "inptText w120",
                    attrs: {
                        name: "secret",
                        type: "text",
                        "data-vv-as": e.$t("ipsec_ikev2.share_secret_key")
                    },
                    domProps: {
                        value: e.tableForm.secret
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.secret = t.target.value)
                        }
                    }
                })]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("secret") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("secret")) + "\n                                        ")]) : e._e()])]) : e._e(), e._v(" "), "mschapv2" == e.tableForm.authby ? a("div", [a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.server_certificate")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("textarea", {
                    directives: [{
                        name: "validate",
                        rawName: "v-validate",
                        value: "required",
                        expression: "'required'"
                    }, {
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.leftcert,
                        expression: "tableForm.leftcert"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "leftcert",
                        "data-vv-as": e.$t("ipsec_ikev2.server_certificate")
                    },
                    domProps: {
                        value: e.tableForm.leftcert
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.leftcert = t.target.value)
                        }
                    }
                })]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("leftcert") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("leftcert")))]) : e._e()]), e._v(" "), a("div", {
                    staticClass: "remark"
                }, [a("p", [1 == e.oemSign ? a("span", [e._v("\n                                                      " + e._s(e.$t("ipsec_ikev2.server_certificate_tip")) + "\n                                                ")]) : a("span", [e._v(e._s(e.$t("ipsec_ikev2.server_certificate_tip2")))])])])]), e._v(" "), a("div", {
                    staticClass: "line_edit"
                }, [a("div", {
                    staticClass: "input_tit"
                }, [e._v(e._s(e.$t("ipsec_ikev2.private_key")) + "：")]), e._v(" "), a("div", {
                    staticClass: "input_group"
                }, [a("textarea", {
                    directives: [{
                        name: "validate",
                        rawName: "v-validate",
                        value: "required",
                        expression: "'required'"
                    }, {
                        name: "model",
                        rawName: "v-model",
                        value: e.tableForm.privatekey,
                        expression: "tableForm.privatekey"
                    }],
                    staticClass: "inptText",
                    attrs: {
                        name: "privatekey",
                        "data-vv-as": e.$t("ipsec_ikev2.private_key")
                    },
                    domProps: {
                        value: e.tableForm.privatekey
                    },
                    on: {
                        input: function(t) {
                            t.target.composing || (e.tableForm.privatekey = t.target.value)
                        }
                    }
                })]), e._v(" "), a("div", {
                    staticClass: "input_P"
                }, [e.errors.has("privatekey") ? a("p", {
                    staticClass: "error_tip"
                }, [e._v(e._s(e.errors.first("privatekey")))]) : e._e()])])]) : e._e(), e._v(" "), "none" == e.tableForm.authby ? a("div") : e._e(), e._v(" "), a("div", {
                    staticClass: "h40"
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
                }, [e._v("\n                                            " + e._s(e.$t("common.save")) + "\n                                        ")])])])])])])])])]) : a("div", [a("div", {
                    staticStyle: {
                        width: "100%",
                        "text-align": "center",
                        "line-height": "150%",
                        "margin-top": "20%",
                        "font-size": "14px"
                    }
                }, [a("i", {
                    staticClass: "ico-mark"
                }), e._v(e._s(e.$t("common.xEnterprise_2")) + "\n            ")])])], 1)
            },
            staticRenderFns: []
        }
    },
    920: function(e, t, a) {
        a(2069);
        var i = a(23)(a(1734), a(2309), "data-v-a30e8126", null);
        e.exports = i.exports
    }
});
