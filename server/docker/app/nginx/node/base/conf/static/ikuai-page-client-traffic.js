webpackJsonp([11], {
    1e3: function(t, e, i) {
        function n(t) {
            a.call(this, t)
        }
        var o = i(1)
          , a = i(999);
        n.prototype = {
            constructor: n,
            type: "cartesian2d",
            dimensions: ["x", "y"],
            getBaseAxis: function() {
                return this.getAxesByScale("ordinal")[0] || this.getAxesByScale("time")[0] || this.getAxis("x")
            },
            containPoint: function(t) {
                var e = this.getAxis("x")
                  , i = this.getAxis("y");
                return e.contain(e.toLocalCoord(t[0])) && i.contain(i.toLocalCoord(t[1]))
            },
            containData: function(t) {
                return this.getAxis("x").containData(t[0]) && this.getAxis("y").containData(t[1])
            },
            dataToPoint: function(t, e, i) {
                var n = this.getAxis("x")
                  , o = this.getAxis("y");
                return i = i || [],
                i[0] = n.toGlobalCoord(n.dataToCoord(t[0])),
                i[1] = o.toGlobalCoord(o.dataToCoord(t[1])),
                i
            },
            clampData: function(t, e) {
                var i = this.getAxis("x").scale
                  , n = this.getAxis("y").scale
                  , o = i.getExtent()
                  , a = n.getExtent()
                  , s = i.parse(t[0])
                  , r = n.parse(t[1]);
                return e = e || [],
                e[0] = Math.min(Math.max(Math.min(o[0], o[1]), s), Math.max(o[0], o[1])),
                e[1] = Math.min(Math.max(Math.min(a[0], a[1]), r), Math.max(a[0], a[1])),
                e
            },
            pointToData: function(t, e) {
                var i = this.getAxis("x")
                  , n = this.getAxis("y");
                return e = e || [],
                e[0] = i.coordToData(i.toLocalCoord(t[0])),
                e[1] = n.coordToData(n.toLocalCoord(t[1])),
                e
            },
            getOtherAxis: function(t) {
                return this.getAxis("x" === t.dim ? "y" : "x")
            }
        },
        o.inherits(n, a);
        var s = n;
        t.exports = s
    },
    1001: function(t, e, i) {
        i(947);
        var n = i(81)
          , o = n.extend({
            type: "grid",
            dependencies: ["xAxis", "yAxis"],
            layoutMode: "box",
            coordinateSystem: null,
            defaultOption: {
                show: !1,
                zlevel: 0,
                z: 0,
                left: "10%",
                top: 60,
                right: "10%",
                bottom: 60,
                containLabel: !1,
                backgroundColor: "rgba(0,0,0,0)",
                borderWidth: 1,
                borderColor: "#ccc"
            }
        });
        t.exports = o
    },
    1004: function(t, e, i) {
        var n = i(24)
          , o = (n.__DEV__,
        i(347))
          , a = i(344)
          , s = a.extend({
            type: "series.line",
            dependencies: ["grid", "polar"],
            getInitialData: function(t, e) {
                return o(this.getSource(), this)
            },
            defaultOption: {
                zlevel: 0,
                z: 2,
                coordinateSystem: "cartesian2d",
                legendHoverLink: !0,
                hoverAnimation: !0,
                clipOverflow: !0,
                label: {
                    position: "top"
                },
                lineStyle: {
                    width: 2,
                    type: "solid"
                },
                step: !1,
                smooth: !1,
                smoothMonotone: null,
                symbol: "emptyCircle",
                symbolSize: 4,
                symbolRotate: null,
                showSymbol: !0,
                showAllSymbol: "auto",
                connectNulls: !1,
                sampling: "none",
                animationEasing: "linear",
                progressive: 0,
                hoverLayerThreshold: 1 / 0
            }
        });
        t.exports = s
    },
    1005: function(t, e, i) {
        function n(t, e) {
            if (t.length === e.length) {
                for (var i = 0; i < t.length; i++) {
                    var n = t[i]
                      , o = e[i];
                    if (n[0] !== o[0] || n[1] !== o[1])
                        return
                }
                return !0
            }
        }
        function o(t) {
            return "number" == typeof t ? t : t ? .5 : 0
        }
        function a(t) {
            var e = t.getGlobalExtent();
            if (t.onBand) {
                var i = t.getBandWidth() / 2 - 1
                  , n = e[1] > e[0] ? 1 : -1;
                e[0] += n * i,
                e[1] -= n * i
            }
            return e
        }
        function s(t, e, i) {
            if (!i.valueDim)
                return [];
            for (var n = [], o = 0, a = e.count(); o < a; o++)
                n.push(M(i, t, e, o));
            return n
        }
        function r(t, e, i, n) {
            var o = a(t.getAxis("x"))
              , s = a(t.getAxis("y"))
              , r = t.getBaseAxis().isHorizontal()
              , l = Math.min(o[0], o[1])
              , c = Math.min(s[0], s[1])
              , d = Math.max(o[0], o[1]) - l
              , u = Math.max(s[0], s[1]) - c;
            if (i)
                l -= .5,
                d += .5,
                c -= .5,
                u += .5;
            else {
                var h = n.get("lineStyle.width") || 2
                  , p = n.get("clipOverflow") ? h / 2 : Math.max(d, u);
                r ? (c -= p,
                u += 2 * p) : (l -= p,
                d += 2 * p)
            }
            var g = new y.Rect({
                shape: {
                    x: l,
                    y: c,
                    width: d,
                    height: u
                }
            });
            return e && (g.shape[r ? "width" : "height"] = 0,
            y.initProps(g, {
                shape: {
                    width: d,
                    height: u
                }
            }, n)),
            g
        }
        function l(t, e, i, n) {
            var o = t.getAngleAxis()
              , a = t.getRadiusAxis()
              , s = a.getExtent().slice();
            s[0] > s[1] && s.reverse();
            var r = o.getExtent()
              , l = Math.PI / 180;
            i && (s[0] -= .5,
            s[1] += .5);
            var c = new y.Sector({
                shape: {
                    cx: T(t.cx, 1),
                    cy: T(t.cy, 1),
                    r0: T(s[0], 1),
                    r: T(s[1], 1),
                    startAngle: -r[0] * l,
                    endAngle: -r[1] * l,
                    clockwise: o.inverse
                }
            });
            return e && (c.shape.endAngle = -r[0] * l,
            y.initProps(c, {
                shape: {
                    endAngle: -r[1] * l
                }
            }, n)),
            c
        }
        function c(t, e, i, n) {
            return "polar" === t.type ? l(t, e, i, n) : r(t, e, i, n)
        }
        function d(t, e, i) {
            for (var n = e.getBaseAxis(), o = "x" === n.dim || "radius" === n.dim ? 0 : 1, a = [], s = 0; s < t.length - 1; s++) {
                var r = t[s + 1]
                  , l = t[s];
                a.push(l);
                var c = [];
                switch (i) {
                case "end":
                    c[o] = r[o],
                    c[1 - o] = l[1 - o],
                    a.push(c);
                    break;
                case "middle":
                    var d = (l[o] + r[o]) / 2
                      , u = [];
                    c[o] = u[o] = d,
                    c[1 - o] = l[1 - o],
                    u[1 - o] = r[1 - o],
                    a.push(c),
                    a.push(u);
                    break;
                default:
                    c[o] = l[o],
                    c[1 - o] = r[1 - o],
                    a.push(c)
                }
            }
            return t[s] && a.push(t[s]),
            a
        }
        function u(t, e) {
            var i = t.getVisual("visualMeta");
            if (i && i.length && t.count() && "cartesian2d" === e.type) {
                for (var n, o, a = i.length - 1; a >= 0; a--) {
                    var s = i[a].dimension
                      , r = t.dimensions[s]
                      , l = t.getDimensionInfo(r);
                    if ("x" === (n = l && l.coordDim) || "y" === n) {
                        o = i[a];
                        break
                    }
                }
                if (o) {
                    var c = e.getAxis(n)
                      , d = f.map(o.stops, function(t) {
                        return {
                            coord: c.toGlobalCoord(c.dataToCoord(t.value)),
                            color: t.color
                        }
                    })
                      , u = d.length
                      , h = o.outerColors.slice();
                    u && d[0].coord > d[u - 1].coord && (d.reverse(),
                    h.reverse());
                    var p = d[0].coord - 10
                      , g = d[u - 1].coord + 10
                      , m = g - p;
                    if (m < .001)
                        return "transparent";
                    f.each(d, function(t) {
                        t.offset = (t.coord - p) / m
                    }),
                    d.push({
                        offset: u ? d[u - 1].offset : .5,
                        color: h[1] || "transparent"
                    }),
                    d.unshift({
                        offset: u ? d[0].offset : .5,
                        color: h[0] || "transparent"
                    });
                    var x = new y.LinearGradient(0,0,0,0,d,!0);
                    return x[n] = p,
                    x[n + "2"] = g,
                    x
                }
            }
        }
        function h(t, e, i) {
            var n = t.get("showAllSymbol")
              , o = "auto" === n;
            if (!n || o) {
                var a = i.getAxesByScale("ordinal")[0];
                if (a && (!o || !p(a, e))) {
                    var s = e.mapDimension(a.dim)
                      , r = {};
                    return f.each(a.getViewLabels(), function(t) {
                        r[t.tickValue] = 1
                    }),
                    function(t) {
                        return !r.hasOwnProperty(e.get(s, t))
                    }
                }
            }
        }
        function p(t, e) {
            var i = t.getExtent()
              , n = Math.abs(i[1] - i[0]) / t.scale.count();
            isNaN(n) && (n = 0);
            for (var o = e.count(), a = Math.max(1, Math.round(o / 5)), s = 0; s < o; s += a)
                if (1.5 * x.getSymbolSize(e, s)[t.isHorizontal() ? 1 : 0] > n)
                    return !1;
            return !0
        }
        var g = i(24)
          , f = (g.__DEV__,
        i(1))
          , m = i(953)
          , x = i(944)
          , v = i(1006)
          , y = i(77)
          , _ = i(11)
          , b = i(982)
          , w = b.Polyline
          , S = b.Polygon
          , A = i(346)
          , C = i(30)
          , T = C.round
          , I = i(956)
          , D = I.prepareDataCoordInfo
          , M = I.getStackedOnPoint
          , O = A.extend({
            type: "line",
            init: function() {
                var t = new y.Group
                  , e = new m;
                this.group.add(e.group),
                this._symbolDraw = e,
                this._lineGroup = t
            },
            render: function(t, e, i) {
                var a = t.coordinateSystem
                  , r = this.group
                  , l = t.getData()
                  , p = t.getModel("lineStyle")
                  , g = t.getModel("areaStyle")
                  , m = l.mapArray(l.getItemLayout)
                  , x = "polar" === a.type
                  , v = this._coordSys
                  , y = this._symbolDraw
                  , _ = this._polyline
                  , b = this._polygon
                  , w = this._lineGroup
                  , S = t.get("animation")
                  , A = !g.isEmpty()
                  , C = g.get("origin")
                  , T = D(a, l, C)
                  , I = s(a, l, T)
                  , M = t.get("showSymbol")
                  , O = M && !x && h(t, l, a)
                  , P = this._data;
                P && P.eachItemGraphicEl(function(t, e) {
                    t.__temp && (r.remove(t),
                    P.setItemGraphicEl(e, null))
                }),
                M || y.remove(),
                r.add(w);
                var k = !x && t.get("step");
                _ && v.type === a.type && k === this._step ? (A && !b ? b = this._newPolygon(m, I, a, S) : b && !A && (w.remove(b),
                b = this._polygon = null),
                w.setClipPath(c(a, !1, !1, t)),
                M && y.updateData(l, {
                    isIgnore: O,
                    clipShape: c(a, !1, !0, t)
                }),
                l.eachItemGraphicEl(function(t) {
                    t.stopAnimation(!0)
                }),
                n(this._stackedOnPoints, I) && n(this._points, m) || (S ? this._updateAnimation(l, I, a, i, k, C) : (k && (m = d(m, a, k),
                I = d(I, a, k)),
                _.setShape({
                    points: m
                }),
                b && b.setShape({
                    points: m,
                    stackedOnPoints: I
                })))) : (M && y.updateData(l, {
                    isIgnore: O,
                    clipShape: c(a, !1, !0, t)
                }),
                k && (m = d(m, a, k),
                I = d(I, a, k)),
                _ = this._newPolyline(m, a, S),
                A && (b = this._newPolygon(m, I, a, S)),
                w.setClipPath(c(a, !0, !1, t)));
                var L = u(l, a) || l.getVisual("color");
                _.useStyle(f.defaults(p.getLineStyle(), {
                    fill: "none",
                    stroke: L,
                    lineJoin: "bevel"
                }));
                var E = t.get("smooth");
                if (E = o(t.get("smooth")),
                _.setShape({
                    smooth: E,
                    smoothMonotone: t.get("smoothMonotone"),
                    connectNulls: t.get("connectNulls")
                }),
                b) {
                    var R = l.getCalculationInfo("stackedOnSeries")
                      , z = 0;
                    b.useStyle(f.defaults(g.getAreaStyle(), {
                        fill: L,
                        opacity: .7,
                        lineJoin: "bevel"
                    })),
                    R && (z = o(R.get("smooth"))),
                    b.setShape({
                        smooth: E,
                        stackedOnSmooth: z,
                        smoothMonotone: t.get("smoothMonotone"),
                        connectNulls: t.get("connectNulls")
                    })
                }
                this._data = l,
                this._coordSys = a,
                this._stackedOnPoints = I,
                this._points = m,
                this._step = k,
                this._valueOrigin = C
            },
            dispose: function() {},
            highlight: function(t, e, i, n) {
                var o = t.getData()
                  , a = _.queryDataIndex(o, n);
                if (!(a instanceof Array) && null != a && a >= 0) {
                    var s = o.getItemGraphicEl(a);
                    if (!s) {
                        var r = o.getItemLayout(a);
                        if (!r)
                            return;
                        s = new x(o,a),
                        s.position = r,
                        s.setZ(t.get("zlevel"), t.get("z")),
                        s.ignore = isNaN(r[0]) || isNaN(r[1]),
                        s.__temp = !0,
                        o.setItemGraphicEl(a, s),
                        s.stopSymbolAnimation(!0),
                        this.group.add(s)
                    }
                    s.highlight()
                } else
                    A.prototype.highlight.call(this, t, e, i, n)
            },
            downplay: function(t, e, i, n) {
                var o = t.getData()
                  , a = _.queryDataIndex(o, n);
                if (null != a && a >= 0) {
                    var s = o.getItemGraphicEl(a);
                    s && (s.__temp ? (o.setItemGraphicEl(a, null),
                    this.group.remove(s)) : s.downplay())
                } else
                    A.prototype.downplay.call(this, t, e, i, n)
            },
            _newPolyline: function(t) {
                var e = this._polyline;
                return e && this._lineGroup.remove(e),
                e = new w({
                    shape: {
                        points: t
                    },
                    silent: !0,
                    z2: 10
                }),
                this._lineGroup.add(e),
                this._polyline = e,
                e
            },
            _newPolygon: function(t, e) {
                var i = this._polygon;
                return i && this._lineGroup.remove(i),
                i = new S({
                    shape: {
                        points: t,
                        stackedOnPoints: e
                    },
                    silent: !0
                }),
                this._lineGroup.add(i),
                this._polygon = i,
                i
            },
            _updateAnimation: function(t, e, i, n, o, a) {
                var s = this._polyline
                  , r = this._polygon
                  , l = t.hostModel
                  , c = v(this._data, t, this._stackedOnPoints, e, this._coordSys, i, this._valueOrigin, a)
                  , u = c.current
                  , h = c.stackedOnCurrent
                  , p = c.next
                  , g = c.stackedOnNext;
                o && (u = d(c.current, i, o),
                h = d(c.stackedOnCurrent, i, o),
                p = d(c.next, i, o),
                g = d(c.stackedOnNext, i, o)),
                s.shape.__points = c.current,
                s.shape.points = u,
                y.updateProps(s, {
                    shape: {
                        points: p
                    }
                }, l),
                r && (r.setShape({
                    points: u,
                    stackedOnPoints: h
                }),
                y.updateProps(r, {
                    shape: {
                        points: p,
                        stackedOnPoints: g
                    }
                }, l));
                for (var f = [], m = c.status, x = 0; x < m.length; x++) {
                    if ("=" === m[x].cmd) {
                        var _ = t.getItemGraphicEl(m[x].idx1);
                        _ && f.push({
                            el: _,
                            ptIdx: x
                        })
                    }
                }
                s.animators && s.animators.length && s.animators[0].during(function() {
                    for (var t = 0; t < f.length; t++) {
                        f[t].el.attr("position", s.shape.__points[f[t].ptIdx])
                    }
                })
            },
            remove: function(t) {
                var e = this.group
                  , i = this._data;
                this._lineGroup.removeAll(),
                this._symbolDraw.remove(!0),
                i && i.eachItemGraphicEl(function(t, n) {
                    t.__temp && (e.remove(t),
                    i.setItemGraphicEl(n, null))
                }),
                this._polyline = this._polygon = this._coordSys = this._points = this._stackedOnPoints = this._data = null
            }
        });
        t.exports = O
    },
    1006: function(t, e, i) {
        function n(t, e) {
            var i = [];
            return e.diff(t).add(function(t) {
                i.push({
                    cmd: "+",
                    idx: t
                })
            }).update(function(t, e) {
                i.push({
                    cmd: "=",
                    idx: e,
                    idx1: t
                })
            }).remove(function(t) {
                i.push({
                    cmd: "-",
                    idx: t
                })
            }).execute(),
            i
        }
        function o(t, e, i, o, a, l, c, d) {
            for (var u = n(t, e), h = [], p = [], g = [], f = [], m = [], x = [], v = [], y = s(a, e, c), _ = s(l, t, d), b = 0; b < u.length; b++) {
                var w = u[b]
                  , S = !0;
                switch (w.cmd) {
                case "=":
                    var A = t.getItemLayout(w.idx)
                      , C = e.getItemLayout(w.idx1);
                    (isNaN(A[0]) || isNaN(A[1])) && (A = C.slice()),
                    h.push(A),
                    p.push(C),
                    g.push(i[w.idx]),
                    f.push(o[w.idx1]),
                    v.push(e.getRawIndex(w.idx1));
                    break;
                case "+":
                    var T = w.idx;
                    h.push(a.dataToPoint([e.get(y.dataDimsForPoint[0], T), e.get(y.dataDimsForPoint[1], T)])),
                    p.push(e.getItemLayout(T).slice()),
                    g.push(r(y, a, e, T)),
                    f.push(o[T]),
                    v.push(e.getRawIndex(T));
                    break;
                case "-":
                    var T = w.idx
                      , I = t.getRawIndex(T);
                    I !== T ? (h.push(t.getItemLayout(T)),
                    p.push(l.dataToPoint([t.get(_.dataDimsForPoint[0], T), t.get(_.dataDimsForPoint[1], T)])),
                    g.push(i[T]),
                    f.push(r(_, l, t, T)),
                    v.push(I)) : S = !1
                }
                S && (m.push(w),
                x.push(x.length))
            }
            x.sort(function(t, e) {
                return v[t] - v[e]
            });
            for (var D = [], M = [], O = [], P = [], k = [], b = 0; b < x.length; b++) {
                var T = x[b];
                D[b] = h[T],
                M[b] = p[T],
                O[b] = g[T],
                P[b] = f[T],
                k[b] = m[T]
            }
            return {
                current: D,
                next: M,
                stackedOnCurrent: O,
                stackedOnNext: P,
                status: k
            }
        }
        var a = i(956)
          , s = a.prepareDataCoordInfo
          , r = a.getStackedOnPoint;
        t.exports = o
    },
    1007: function(t, e, i) {
        var n = i(343)
          , o = n.extendComponentModel({
            type: "axisPointer",
            coordSysAxesInfo: null,
            defaultOption: {
                show: "auto",
                triggerOn: null,
                zlevel: 0,
                z: 50,
                type: "line",
                snap: !1,
                triggerTooltip: !0,
                value: null,
                status: null,
                link: [],
                animation: null,
                animationDurationUpdate: 200,
                lineStyle: {
                    color: "#aaa",
                    width: 1,
                    type: "solid"
                },
                shadowStyle: {
                    color: "rgba(150,150,150,0.3)"
                },
                label: {
                    show: !0,
                    formatter: null,
                    precision: "auto",
                    margin: 3,
                    color: "#fff",
                    padding: [5, 7, 5, 7],
                    backgroundColor: "auto",
                    borderColor: null,
                    borderWidth: 0,
                    shadowBlur: 3,
                    shadowColor: "#aaa"
                },
                handle: {
                    show: !1,
                    icon: "M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7v-1.2h6.6z M13.3,22H6.7v-1.2h6.6z M13.3,19.6H6.7v-1.2h6.6z",
                    size: 45,
                    margin: 50,
                    color: "#333",
                    shadowBlur: 3,
                    shadowColor: "#aaa",
                    shadowOffsetX: 0,
                    shadowOffsetY: 2,
                    throttle: 40
                }
            }
        })
          , a = o;
        t.exports = a
    },
    1008: function(t, e, i) {
        var n = i(343)
          , o = i(958)
          , a = n.extendComponentView({
            type: "axisPointer",
            render: function(t, e, i) {
                var n = e.getComponent("tooltip")
                  , a = t.get("triggerOn") || n && n.get("triggerOn") || "mousemove|click";
                o.register("axisPointer", i, function(t, e, i) {
                    "none" !== a && ("leave" === t || a.indexOf(t) >= 0) && i({
                        type: "updateAxisPointer",
                        currTrigger: t,
                        x: e && e.offsetX,
                        y: e && e.offsetY
                    })
                })
            },
            remove: function(t, e) {
                o.unregister(e.getZr(), "axisPointer"),
                a.superApply(this._model, "remove", arguments)
            },
            dispose: function(t, e) {
                o.unregister("axisPointer", e),
                a.superApply(this._model, "dispose", arguments)
            }
        })
          , s = a;
        t.exports = s
    },
    1009: function(t, e, i) {
        function n(t, e, i) {
            var n = t.currTrigger
              , a = [t.x, t.y]
              , f = t
              , m = t.dispatchAction || g.bind(i.dispatchAction, i)
              , x = e.getComponent("axisPointer").coordSysAxesInfo;
            if (x) {
                p(a) && (a = v({
                    seriesIndex: f.seriesIndex,
                    dataIndex: f.dataIndex
                }, e).point);
                var b = p(a)
                  , w = f.axesInfo
                  , S = x.axesInfo
                  , A = "leave" === n || p(a)
                  , C = {}
                  , T = {}
                  , I = {
                    list: [],
                    map: {}
                }
                  , D = {
                    showPointer: _(s, T),
                    showTooltip: _(r, I)
                };
                y(x.coordSysMap, function(t, e) {
                    var i = b || t.containPoint(a);
                    y(x.coordSysAxesInfo[e], function(t, e) {
                        var n = t.axis
                          , s = u(w, t);
                        if (!A && i && (!w || s)) {
                            var r = s && s.value;
                            null != r || b || (r = n.pointToData(a)),
                            null != r && o(t, r, D, !1, C)
                        }
                    })
                });
                var M = {};
                return y(S, function(t, e) {
                    var i = t.linkGroup;
                    i && !T[e] && y(i.axesInfo, function(e, n) {
                        var o = T[n];
                        if (e !== t && o) {
                            var a = o.value;
                            i.mapper && (a = t.axis.scale.parse(i.mapper(a, h(e), h(t)))),
                            M[t.key] = a
                        }
                    })
                }),
                y(M, function(t, e) {
                    o(S[e], t, D, !0, C)
                }),
                l(T, S, C),
                c(I, a, t, m),
                d(S, m, i),
                C
            }
        }
        function o(t, e, i, n, o) {
            var s = t.axis;
            if (!s.scale.isBlank() && s.containData(e)) {
                if (!t.involveSeries)
                    return void i.showPointer(t, e);
                var r = a(e, t)
                  , l = r.payloadBatch
                  , c = r.snapToValue;
                l[0] && null == o.seriesIndex && g.extend(o, l[0]),
                !n && t.snap && s.containData(c) && null != c && (e = c),
                i.showPointer(t, e, l, o),
                i.showTooltip(t, r, c)
            }
        }
        function a(t, e) {
            var i = e.axis
              , n = i.dim
              , o = t
              , a = []
              , s = Number.MAX_VALUE
              , r = -1;
            return y(e.seriesModels, function(e, l) {
                var c, d, u = e.getData().mapDimension(n, !0);
                if (e.getAxisTooltipData) {
                    var h = e.getAxisTooltipData(u, t, i);
                    d = h.dataIndices,
                    c = h.nestestValue
                } else {
                    if (d = e.getData().indicesOfNearest(u[0], t, "category" === i.type ? .5 : null),
                    !d.length)
                        return;
                    c = e.getData().get(u[0], d[0])
                }
                if (null != c && isFinite(c)) {
                    var p = t - c
                      , g = Math.abs(p);
                    g <= s && ((g < s || p >= 0 && r < 0) && (s = g,
                    r = p,
                    o = c,
                    a.length = 0),
                    y(d, function(t) {
                        a.push({
                            seriesIndex: e.seriesIndex,
                            dataIndexInside: t,
                            dataIndex: e.getData().getRawIndex(t)
                        })
                    }))
                }
            }),
            {
                payloadBatch: a,
                snapToValue: o
            }
        }
        function s(t, e, i, n) {
            t[e.key] = {
                value: i,
                payloadBatch: n
            }
        }
        function r(t, e, i, n) {
            var o = i.payloadBatch
              , a = e.axis
              , s = a.model
              , r = e.axisPointerModel;
            if (e.triggerTooltip && o.length) {
                var l = e.coordSys.model
                  , c = x.makeKey(l)
                  , d = t.map[c];
                d || (d = t.map[c] = {
                    coordSysId: l.id,
                    coordSysIndex: l.componentIndex,
                    coordSysType: l.type,
                    coordSysMainType: l.mainType,
                    dataByAxis: []
                },
                t.list.push(d)),
                d.dataByAxis.push({
                    axisDim: a.dim,
                    axisIndex: s.componentIndex,
                    axisType: s.type,
                    axisId: s.id,
                    value: n,
                    valueLabelOpt: {
                        precision: r.get("label.precision"),
                        formatter: r.get("label.formatter")
                    },
                    seriesDataIndices: o.slice()
                })
            }
        }
        function l(t, e, i) {
            var n = i.axesInfo = [];
            y(e, function(e, i) {
                var o = e.axisPointerModel.option
                  , a = t[i];
                a ? (!e.useHandle && (o.status = "show"),
                o.value = a.value,
                o.seriesDataIndices = (a.payloadBatch || []).slice()) : !e.useHandle && (o.status = "hide"),
                "show" === o.status && n.push({
                    axisDim: e.axis.dim,
                    axisIndex: e.axis.model.componentIndex,
                    value: o.value
                })
            })
        }
        function c(t, e, i, n) {
            if (p(e) || !t.list.length)
                return void n({
                    type: "hideTip"
                });
            var o = ((t.list[0].dataByAxis[0] || {}).seriesDataIndices || [])[0] || {};
            n({
                type: "showTip",
                escapeConnect: !0,
                x: e[0],
                y: e[1],
                tooltipOption: i.tooltipOption,
                position: i.position,
                dataIndexInside: o.dataIndexInside,
                dataIndex: o.dataIndex,
                seriesIndex: o.seriesIndex,
                dataByCoordSys: t.list
            })
        }
        function d(t, e, i) {
            var n = i.getZr()
              , o = b(n).axisPointerLastHighlights || {}
              , a = b(n).axisPointerLastHighlights = {};
            y(t, function(t, e) {
                var i = t.axisPointerModel.option;
                "show" === i.status && y(i.seriesDataIndices, function(t) {
                    var e = t.seriesIndex + " | " + t.dataIndex;
                    a[e] = t
                })
            });
            var s = []
              , r = [];
            g.each(o, function(t, e) {
                !a[e] && r.push(t)
            }),
            g.each(a, function(t, e) {
                !o[e] && s.push(t)
            }),
            r.length && i.dispatchAction({
                type: "downplay",
                escapeConnect: !0,
                batch: r
            }),
            s.length && i.dispatchAction({
                type: "highlight",
                escapeConnect: !0,
                batch: s
            })
        }
        function u(t, e) {
            for (var i = 0; i < (t || []).length; i++) {
                var n = t[i];
                if (e.axis.dim === n.axisDim && e.axis.model.componentIndex === n.axisIndex)
                    return n
            }
        }
        function h(t) {
            var e = t.axis.model
              , i = {}
              , n = i.axisDim = t.axis.dim;
            return i.axisIndex = i[n + "AxisIndex"] = e.componentIndex,
            i.axisName = i[n + "AxisName"] = e.name,
            i.axisId = i[n + "AxisId"] = e.id,
            i
        }
        function p(t) {
            return !t || null == t[0] || isNaN(t[0]) || null == t[1] || isNaN(t[1])
        }
        var g = i(1)
          , f = i(11)
          , m = f.makeInner
          , x = i(936)
          , v = i(957)
          , y = g.each
          , _ = g.curry
          , b = m();
        t.exports = n
    },
    1010: function(t, e, i) {
        function n(t, e, i) {
            var n, o = {}, s = "toggleSelected" === t;
            return i.eachComponent("legend", function(i) {
                s && null != n ? i[n ? "select" : "unSelect"](e.name) : (i[t](e.name),
                n = i.isSelected(e.name));
                var r = i.getData();
                a.each(r, function(t) {
                    var e = t.get("name");
                    if ("\n" !== e && "" !== e) {
                        var n = i.isSelected(e);
                        o.hasOwnProperty(e) ? o[e] = o[e] && n : o[e] = n
                    }
                })
            }),
            {
                name: e.name,
                selected: o
            }
        }
        var o = i(343)
          , a = i(1);
        o.registerAction("legendToggleSelect", "legendselectchanged", a.curry(n, "toggleSelected")),
        o.registerAction("legendSelect", "legendselected", a.curry(n, "select")),
        o.registerAction("legendUnSelect", "legendunselected", a.curry(n, "unSelect"))
    },
    1011: function(t, e) {
        function i(t) {
            var e = t.findComponents({
                mainType: "legend"
            });
            e && e.length && t.filterSeries(function(t) {
                for (var i = 0; i < e.length; i++)
                    if (!e[i].isSelected(t.name))
                        return !1;
                return !0
            })
        }
        t.exports = i
    },
    1012: function(t, e, i) {
        function n(t) {
            var e = "left " + t + "s cubic-bezier(0.23, 1, 0.32, 1),top " + t + "s cubic-bezier(0.23, 1, 0.32, 1)";
            return r.map(g, function(t) {
                return t + "transition:" + e
            }).join(";")
        }
        function o(t) {
            var e = []
              , i = t.get("fontSize")
              , n = t.getTextColor();
            return n && e.push("color:" + n),
            e.push("font:" + t.getFont()),
            i && e.push("line-height:" + Math.round(3 * i / 2) + "px"),
            h(["decoration", "align"], function(i) {
                var n = t.get(i);
                n && e.push("text-" + i + ":" + n)
            }),
            e.join(";")
        }
        function a(t) {
            var e = []
              , i = t.get("transitionDuration")
              , a = t.get("backgroundColor")
              , s = t.getModel("textStyle")
              , r = t.get("padding");
            return i && e.push(n(i)),
            a && (d.canvasSupported ? e.push("background-Color:" + a) : (e.push("background-Color:#" + l.toHex(a)),
            e.push("filter:alpha(opacity=70)"))),
            h(["width", "color", "radius"], function(i) {
                var n = "border-" + i
                  , o = p(n)
                  , a = t.get(o);
                null != a && e.push(n + ":" + a + ("color" === i ? "" : "px"))
            }),
            e.push(o(s)),
            null != r && e.push("padding:" + u.normalizeCssArray(r).join("px ") + "px"),
            e.join(";") + ";"
        }
        function s(t, e) {
            if (d.wxa)
                return null;
            var i = document.createElement("div")
              , n = this._zr = e.getZr();
            this.el = i,
            this._x = e.getWidth() / 2,
            this._y = e.getHeight() / 2,
            t.appendChild(i),
            this._container = t,
            this._show = !1,
            this._hideTimeout;
            var o = this;
            i.onmouseenter = function() {
                o._enterable && (clearTimeout(o._hideTimeout),
                o._show = !0),
                o._inContent = !0
            }
            ,
            i.onmousemove = function(e) {
                if (e = e || window.event,
                !o._enterable) {
                    var i = n.handler;
                    c.normalizeEvent(t, e, !0),
                    i.dispatch("mousemove", e)
                }
            }
            ,
            i.onmouseleave = function() {
                o._enterable && o._show && o.hideLater(o._hideDelay),
                o._inContent = !1
            }
        }
        var r = i(1)
          , l = i(101)
          , c = i(100)
          , d = i(31)
          , u = i(68)
          , h = r.each
          , p = u.toCamelCase
          , g = ["", "-webkit-", "-moz-", "-o-"];
        s.prototype = {
            constructor: s,
            _enterable: !0,
            update: function() {
                var t = this._container
                  , e = t.currentStyle || document.defaultView.getComputedStyle(t)
                  , i = t.style;
                "absolute" !== i.position && "absolute" !== e.position && (i.position = "relative")
            },
            show: function(t) {
                clearTimeout(this._hideTimeout);
                var e = this.el;
                e.style.cssText = "position:absolute;display:block;border-style:solid;white-space:nowrap;z-index:9999999;" + a(t) + ";left:" + this._x + "px;top:" + this._y + "px;" + (t.get("extraCssText") || ""),
                e.style.display = e.innerHTML ? "block" : "none",
                e.style.pointerEvents = this._enterable ? "auto" : "none",
                this._show = !0
            },
            setContent: function(t) {
                this.el.innerHTML = null == t ? "" : t
            },
            setEnterable: function(t) {
                this._enterable = t
            },
            getSize: function() {
                var t = this.el;
                return [t.clientWidth, t.clientHeight]
            },
            moveTo: function(t, e) {
                var i, n = this._zr;
                n && n.painter && (i = n.painter.getViewportRootOffset()) && (t += i.offsetLeft,
                e += i.offsetTop);
                var o = this.el.style;
                o.left = t + "px",
                o.top = e + "px",
                this._x = t,
                this._y = e
            },
            hide: function() {
                this.el.style.display = "none",
                this._show = !1
            },
            hideLater: function(t) {
                !this._show || this._inContent && this._enterable || (t ? (this._hideDelay = t,
                this._show = !1,
                this._hideTimeout = setTimeout(r.bind(this.hide, this), t)) : this.hide())
            },
            isShow: function() {
                return this._show
            },
            getOuterSize: function() {
                var t = this.el.clientWidth
                  , e = this.el.clientHeight;
                if (document.defaultView && document.defaultView.getComputedStyle) {
                    var i = document.defaultView.getComputedStyle(this.el);
                    i && (t += parseInt(i.paddingLeft, 10) + parseInt(i.paddingRight, 10) + parseInt(i.borderLeftWidth, 10) + parseInt(i.borderRightWidth, 10),
                    e += parseInt(i.paddingTop, 10) + parseInt(i.paddingBottom, 10) + parseInt(i.borderTopWidth, 10) + parseInt(i.borderBottomWidth, 10))
                }
                return {
                    width: t,
                    height: e
                }
            }
        };
        var f = s;
        t.exports = f
    },
    1013: function(t, e, i) {
        var n = i(343)
          , o = n.extendComponentModel({
            type: "tooltip",
            dependencies: ["axisPointer"],
            defaultOption: {
                zlevel: 0,
                z: 60,
                show: !0,
                showContent: !0,
                trigger: "item",
                triggerOn: "mousemove|click",
                alwaysShowContent: !1,
                displayMode: "single",
                renderMode: "auto",
                confine: !1,
                showDelay: 0,
                hideDelay: 100,
                transitionDuration: .4,
                enterable: !1,
                backgroundColor: "rgba(50,50,50,0.7)",
                borderColor: "#333",
                borderRadius: 4,
                borderWidth: 0,
                padding: 5,
                extraCssText: "",
                axisPointer: {
                    type: "line",
                    axis: "auto",
                    animation: "auto",
                    animationDurationUpdate: 200,
                    animationEasingUpdate: "exponentialOut",
                    crossStyle: {
                        color: "#999",
                        width: 1,
                        type: "dashed",
                        textStyle: {}
                    }
                },
                textStyle: {
                    color: "#fff",
                    fontSize: 14
                }
            }
        });
        t.exports = o
    },
    1014: function(t, e, i) {
        function n(t) {
            this._zr = t.getZr(),
            this._show = !1,
            this._hideTimeout
        }
        var o = i(1)
          , a = i(212);
        n.prototype = {
            constructor: n,
            _enterable: !0,
            update: function() {},
            show: function(t) {
                this._hideTimeout && clearTimeout(this._hideTimeout),
                this.el.attr("show", !0),
                this._show = !0
            },
            setContent: function(t, e, i) {
                this.el && this._zr.remove(this.el);
                for (var n = {}, o = t, s = o.indexOf("{marker"); s >= 0; ) {
                    var r = o.indexOf("|}")
                      , l = o.substr(s + "{marker".length, r - s - "{marker".length);
                    l.indexOf("sub") > -1 ? n["marker" + l] = {
                        textWidth: 4,
                        textHeight: 4,
                        textBorderRadius: 2,
                        textBackgroundColor: e[l],
                        textOffset: [3, 0]
                    } : n["marker" + l] = {
                        textWidth: 10,
                        textHeight: 10,
                        textBorderRadius: 5,
                        textBackgroundColor: e[l]
                    },
                    o = o.substr(r + 1),
                    s = o.indexOf("{marker")
                }
                this.el = new a({
                    style: {
                        rich: n,
                        text: t,
                        textLineHeight: 20,
                        textBackgroundColor: i.get("backgroundColor"),
                        textBorderRadius: i.get("borderRadius"),
                        textFill: i.get("textStyle.color"),
                        textPadding: i.get("padding")
                    },
                    z: i.get("z")
                }),
                this._zr.add(this.el);
                var c = this;
                this.el.on("mouseover", function() {
                    c._enterable && (clearTimeout(c._hideTimeout),
                    c._show = !0),
                    c._inContent = !0
                }),
                this.el.on("mouseout", function() {
                    c._enterable && c._show && c.hideLater(c._hideDelay),
                    c._inContent = !1
                })
            },
            setEnterable: function(t) {
                this._enterable = t
            },
            getSize: function() {
                var t = this.el.getBoundingRect();
                return [t.width, t.height]
            },
            moveTo: function(t, e) {
                this.el && this.el.attr("position", [t, e])
            },
            hide: function() {
                this.el.hide(),
                this._show = !1
            },
            hideLater: function(t) {
                !this._show || this._inContent && this._enterable || (t ? (this._hideDelay = t,
                this._show = !1,
                this._hideTimeout = setTimeout(o.bind(this.hide, this), t)) : this.hide())
            },
            isShow: function() {
                return this._show
            },
            getOuterSize: function() {
                return this.getSize()
            }
        };
        var s = n;
        t.exports = s
    },
    1015: function(t, e, i) {
        function n(t) {
            for (var e = t.pop(); t.length; ) {
                var i = t.pop();
                i && (y.isInstance(i) && (i = i.get("tooltip", !0)),
                "string" == typeof i && (i = {
                    formatter: i
                }),
                e = new y(i,e,e.ecModel))
            }
            return e
        }
        function o(t, e) {
            return t.dispatchAction || d.bind(e.dispatchAction, e)
        }
        function a(t, e, i, n, o, a, s) {
            var r = i.getOuterSize()
              , l = r.width
              , c = r.height;
            return null != a && (t + l + a > n ? t -= l + a : t += a),
            null != s && (e + c + s > o ? e -= c + s : e += s),
            [t, e]
        }
        function s(t, e, i, n, o) {
            var a = i.getOuterSize()
              , s = a.width
              , r = a.height;
            return t = Math.min(t + s, n) - s,
            e = Math.min(e + r, o) - r,
            t = Math.max(t, 0),
            e = Math.max(e, 0),
            [t, e]
        }
        function r(t, e, i) {
            var n = i[0]
              , o = i[1]
              , a = 0
              , s = 0
              , r = e.width
              , l = e.height;
            switch (t) {
            case "inside":
                a = e.x + r / 2 - n / 2,
                s = e.y + l / 2 - o / 2;
                break;
            case "top":
                a = e.x + r / 2 - n / 2,
                s = e.y - o - 5;
                break;
            case "bottom":
                a = e.x + r / 2 - n / 2,
                s = e.y + l + 5;
                break;
            case "left":
                a = e.x - n - 5,
                s = e.y + l / 2 - o / 2;
                break;
            case "right":
                a = e.x + r + 5,
                s = e.y + l / 2 - o / 2
            }
            return [a, s]
        }
        function l(t) {
            return "center" === t || "middle" === t
        }
        var c = i(343)
          , d = i(1)
          , u = i(31)
          , h = i(1012)
          , p = i(1014)
          , g = i(68)
          , f = i(30)
          , m = i(77)
          , x = i(957)
          , v = i(132)
          , y = i(82)
          , _ = i(958)
          , b = i(206)
          , w = i(945)
          , S = i(11)
          , A = S.getTooltipRenderMode
          , C = d.bind
          , T = d.each
          , I = f.parsePercent
          , D = new m.Rect({
            shape: {
                x: -1,
                y: -1,
                width: 2,
                height: 2
            }
        })
          , M = c.extendComponentView({
            type: "tooltip",
            init: function(t, e) {
                if (!u.node) {
                    var i = t.getComponent("tooltip")
                      , n = i.get("renderMode");
                    this._renderMode = A(n);
                    var o;
                    "html" === this._renderMode ? (o = new h(e.getDom(),e),
                    this._newLine = "<br/>") : (o = new p(e),
                    this._newLine = "\n"),
                    this._tooltipContent = o
                }
            },
            render: function(t, e, i) {
                if (!u.node) {
                    this.group.removeAll(),
                    this._tooltipModel = t,
                    this._ecModel = e,
                    this._api = i,
                    this._lastDataByCoordSys = null,
                    this._alwaysShowContent = t.get("alwaysShowContent");
                    var n = this._tooltipContent;
                    n.update(),
                    n.setEnterable(t.get("enterable")),
                    this._initGlobalListener(),
                    this._keepShow()
                }
            },
            _initGlobalListener: function() {
                var t = this._tooltipModel
                  , e = t.get("triggerOn");
                _.register("itemTooltip", this._api, C(function(t, i, n) {
                    "none" !== e && (e.indexOf(t) >= 0 ? this._tryShow(i, n) : "leave" === t && this._hide(n))
                }, this))
            },
            _keepShow: function() {
                var t = this._tooltipModel
                  , e = this._ecModel
                  , i = this._api;
                if (null != this._lastX && null != this._lastY && "none" !== t.get("triggerOn")) {
                    var n = this;
                    clearTimeout(this._refreshUpdateTimeout),
                    this._refreshUpdateTimeout = setTimeout(function() {
                        n.manuallyShowTip(t, e, i, {
                            x: n._lastX,
                            y: n._lastY
                        })
                    })
                }
            },
            manuallyShowTip: function(t, e, i, n) {
                if (n.from !== this.uid && !u.node) {
                    var a = o(n, i);
                    this._ticket = "";
                    var s = n.dataByCoordSys;
                    if (n.tooltip && null != n.x && null != n.y) {
                        var r = D;
                        r.position = [n.x, n.y],
                        r.update(),
                        r.tooltip = n.tooltip,
                        this._tryShow({
                            offsetX: n.x,
                            offsetY: n.y,
                            target: r
                        }, a)
                    } else if (s)
                        this._tryShow({
                            offsetX: n.x,
                            offsetY: n.y,
                            position: n.position,
                            event: {},
                            dataByCoordSys: n.dataByCoordSys,
                            tooltipOption: n.tooltipOption
                        }, a);
                    else if (null != n.seriesIndex) {
                        if (this._manuallyAxisShowTip(t, e, i, n))
                            return;
                        var l = x(n, e)
                          , c = l.point[0]
                          , d = l.point[1];
                        null != c && null != d && this._tryShow({
                            offsetX: c,
                            offsetY: d,
                            position: n.position,
                            target: l.el,
                            event: {}
                        }, a)
                    } else
                        null != n.x && null != n.y && (i.dispatchAction({
                            type: "updateAxisPointer",
                            x: n.x,
                            y: n.y
                        }),
                        this._tryShow({
                            offsetX: n.x,
                            offsetY: n.y,
                            position: n.position,
                            target: i.getZr().findHover(n.x, n.y).target,
                            event: {}
                        }, a))
                }
            },
            manuallyHideTip: function(t, e, i, n) {
                var a = this._tooltipContent;
                !this._alwaysShowContent && this._tooltipModel && a.hideLater(this._tooltipModel.get("hideDelay")),
                this._lastX = this._lastY = null,
                n.from !== this.uid && this._hide(o(n, i))
            },
            _manuallyAxisShowTip: function(t, e, i, o) {
                var a = o.seriesIndex
                  , s = o.dataIndex
                  , r = e.getComponent("axisPointer").coordSysAxesInfo;
                if (null != a && null != s && null != r) {
                    var l = e.getSeriesByIndex(a);
                    if (l) {
                        var c = l.getData()
                          , t = n([c.getItemModel(s), l, (l.coordinateSystem || {}).model, t]);
                        if ("axis" === t.get("trigger"))
                            return i.dispatchAction({
                                type: "updateAxisPointer",
                                seriesIndex: a,
                                dataIndex: s,
                                position: o.position
                            }),
                            !0
                    }
                }
            },
            _tryShow: function(t, e) {
                var i = t.target;
                if (this._tooltipModel) {
                    this._lastX = t.offsetX,
                    this._lastY = t.offsetY;
                    var n = t.dataByCoordSys;
                    n && n.length ? this._showAxisTooltip(n, t) : i && null != i.dataIndex ? (this._lastDataByCoordSys = null,
                    this._showSeriesItemTooltip(t, i, e)) : i && i.tooltip ? (this._lastDataByCoordSys = null,
                    this._showComponentItemTooltip(t, i, e)) : (this._lastDataByCoordSys = null,
                    this._hide(e))
                }
            },
            _showOrMove: function(t, e) {
                var i = t.get("showDelay");
                e = d.bind(e, this),
                clearTimeout(this._showTimout),
                i > 0 ? this._showTimout = setTimeout(e, i) : e()
            },
            _showAxisTooltip: function(t, e) {
                var i = this._ecModel
                  , o = this._tooltipModel
                  , a = [e.offsetX, e.offsetY]
                  , s = []
                  , r = []
                  , l = n([e.tooltipOption, o])
                  , c = this._renderMode
                  , u = this._newLine
                  , h = {};
                T(t, function(t) {
                    T(t.dataByAxis, function(t) {
                        var e = i.getComponent(t.axisDim + "Axis", t.axisIndex)
                          , n = t.value
                          , o = [];
                        if (e && null != n) {
                            var a = w.getValueLabel(n, e.axis, i, t.seriesDataIndices, t.valueLabelOpt);
                            d.each(t.seriesDataIndices, function(s) {
                                var l = i.getSeriesByIndex(s.seriesIndex)
                                  , u = s.dataIndexInside
                                  , p = l && l.getDataParams(u);
                                if (p.axisDim = t.axisDim,
                                p.axisIndex = t.axisIndex,
                                p.axisType = t.axisType,
                                p.axisId = t.axisId,
                                p.axisValue = b.getAxisRawValue(e.axis, n),
                                p.axisValueLabel = a,
                                p) {
                                    r.push(p);
                                    var g, f = l.formatTooltip(u, !0, null, c);
                                    if (d.isObject(f)) {
                                        g = f.html;
                                        var m = f.markers;
                                        d.merge(h, m)
                                    } else
                                        g = f;
                                    o.push(g)
                                }
                            });
                            var l = a;
                            "html" !== c ? s.push(o.join(u)) : s.push((l ? g.encodeHTML(l) + u : "") + o.join(u))
                        }
                    })
                }, this),
                s.reverse(),
                s = s.join(this._newLine + this._newLine);
                var p = e.position;
                this._showOrMove(l, function() {
                    this._updateContentNotChangedOnAxis(t) ? this._updatePosition(l, p, a[0], a[1], this._tooltipContent, r) : this._showTooltipContent(l, s, r, Math.random(), a[0], a[1], p, void 0, h)
                })
            },
            _showSeriesItemTooltip: function(t, e, i) {
                var o = this._ecModel
                  , a = e.seriesIndex
                  , s = o.getSeriesByIndex(a)
                  , r = e.dataModel || s
                  , l = e.dataIndex
                  , c = e.dataType
                  , u = r.getData()
                  , h = n([u.getItemModel(l), r, s && (s.coordinateSystem || {}).model, this._tooltipModel])
                  , p = h.get("trigger");
                if (null == p || "item" === p) {
                    var g, f, m = r.getDataParams(l, c), x = r.formatTooltip(l, !1, c, this._renderMode);
                    d.isObject(x) ? (g = x.html,
                    f = x.markers) : (g = x,
                    f = null);
                    var v = "item_" + r.name + "_" + l;
                    this._showOrMove(h, function() {
                        this._showTooltipContent(h, g, m, v, t.offsetX, t.offsetY, t.position, t.target, f)
                    }),
                    i({
                        type: "showTip",
                        dataIndexInside: l,
                        dataIndex: u.getRawIndex(l),
                        seriesIndex: a,
                        from: this.uid
                    })
                }
            },
            _showComponentItemTooltip: function(t, e, i) {
                var n = e.tooltip;
                if ("string" == typeof n) {
                    var o = n;
                    n = {
                        content: o,
                        formatter: o
                    }
                }
                var a = new y(n,this._tooltipModel,this._ecModel)
                  , s = a.get("content")
                  , r = Math.random();
                this._showOrMove(a, function() {
                    this._showTooltipContent(a, s, a.get("formatterParams") || {}, r, t.offsetX, t.offsetY, t.position, e)
                }),
                i({
                    type: "showTip",
                    from: this.uid
                })
            },
            _showTooltipContent: function(t, e, i, n, o, a, s, r, l) {
                if (this._ticket = "",
                t.get("showContent") && t.get("show")) {
                    var c = this._tooltipContent
                      , d = t.get("formatter");
                    s = s || t.get("position");
                    var u = e;
                    if (d && "string" == typeof d)
                        u = g.formatTpl(d, i, !0);
                    else if ("function" == typeof d) {
                        var h = C(function(e, n) {
                            e === this._ticket && (c.setContent(n, l, t),
                            this._updatePosition(t, s, o, a, c, i, r))
                        }, this);
                        this._ticket = n,
                        u = d(i, n, h)
                    }
                    c.setContent(u, l, t),
                    c.show(t),
                    this._updatePosition(t, s, o, a, c, i, r)
                }
            },
            _updatePosition: function(t, e, i, n, o, c, u) {
                var h = this._api.getWidth()
                  , p = this._api.getHeight();
                e = e || t.get("position");
                var g = o.getSize()
                  , f = t.get("align")
                  , m = t.get("verticalAlign")
                  , x = u && u.getBoundingRect().clone();
                if (u && x.applyTransform(u.transform),
                "function" == typeof e && (e = e([i, n], c, o.el, x, {
                    viewSize: [h, p],
                    contentSize: g.slice()
                })),
                d.isArray(e))
                    i = I(e[0], h),
                    n = I(e[1], p);
                else if (d.isObject(e)) {
                    e.width = g[0],
                    e.height = g[1];
                    var y = v.getLayoutRect(e, {
                        width: h,
                        height: p
                    });
                    i = y.x,
                    n = y.y,
                    f = null,
                    m = null
                } else if ("string" == typeof e && u) {
                    var _ = r(e, x, g);
                    i = _[0],
                    n = _[1]
                } else {
                    var _ = a(i, n, o, h, p, f ? null : 20, m ? null : 20);
                    i = _[0],
                    n = _[1]
                }
                if (f && (i -= l(f) ? g[0] / 2 : "right" === f ? g[0] : 0),
                m && (n -= l(m) ? g[1] / 2 : "bottom" === m ? g[1] : 0),
                t.get("confine")) {
                    var _ = s(i, n, o, h, p);
                    i = _[0],
                    n = _[1]
                }
                o.moveTo(i, n)
            },
            _updateContentNotChangedOnAxis: function(t) {
                var e = this._lastDataByCoordSys
                  , i = !!e && e.length === t.length;
                return i && T(e, function(e, n) {
                    var o = e.dataByAxis || {}
                      , a = t[n] || {}
                      , s = a.dataByAxis || [];
                    (i &= o.length === s.length) && T(o, function(t, e) {
                        var n = s[e] || {}
                          , o = t.seriesDataIndices || []
                          , a = n.seriesDataIndices || [];
                        (i &= t.value === n.value && t.axisType === n.axisType && t.axisId === n.axisId && o.length === a.length) && T(o, function(t, e) {
                            var n = a[e];
                            i &= t.seriesIndex === n.seriesIndex && t.dataIndex === n.dataIndex
                        })
                    })
                }),
                this._lastDataByCoordSys = t,
                !!i
            },
            _hide: function(t) {
                this._lastDataByCoordSys = null,
                t({
                    type: "hideTip",
                    from: this.uid
                })
            },
            dispose: function(t, e) {
                u.node || (this._tooltipContent.hide(),
                _.unregister("itemTooltip", e))
            }
        });
        t.exports = M
    },
    1016: function(t, e) {
        function i(t) {
            return {
                seriesType: t,
                modifyOutputEnd: !0,
                reset: function(t, e, i) {
                    var a = t.getData()
                      , s = t.get("sampling")
                      , r = t.coordinateSystem;
                    if ("cartesian2d" === r.type && s) {
                        var l = r.getBaseAxis()
                          , c = r.getOtherAxis(l)
                          , d = l.getExtent()
                          , u = d[1] - d[0]
                          , h = Math.round(a.count() / u);
                        if (h > 1) {
                            var p;
                            "string" == typeof s ? p = n[s] : "function" == typeof s && (p = s),
                            p && t.setData(a.downSample(a.mapDimension(c.dim), 1 / h, p, o))
                        }
                    }
                }
            }
        }
        var n = {
            average: function(t) {
                for (var e = 0, i = 0, n = 0; n < t.length; n++)
                    isNaN(t[n]) || (e += t[n],
                    i++);
                return 0 === i ? NaN : e / i
            },
            sum: function(t) {
                for (var e = 0, i = 0; i < t.length; i++)
                    e += t[i] || 0;
                return e
            },
            max: function(t) {
                for (var e = -1 / 0, i = 0; i < t.length; i++)
                    t[i] > e && (e = t[i]);
                return isFinite(e) ? e : NaN
            },
            min: function(t) {
                for (var e = 1 / 0, i = 0; i < t.length; i++)
                    t[i] < e && (e = t[i]);
                return isFinite(e) ? e : NaN
            },
            nearest: function(t) {
                return t[0]
            }
        }
          , o = function(t, e) {
            return Math.round(t.length / 2)
        };
        t.exports = i
    },
    1091: function(t, e, i) {
        t.exports = {
            default: i(1150),
            __esModule: !0
        }
    },
    1150: function(t, e, i) {
        i(134),
        i(1154),
        t.exports = i(18).Array.from
    },
    1152: function(t, e, i) {
        "use strict";
        var n = i(36)
          , o = i(104);
        t.exports = function(t, e, i) {
            e in t ? n.f(t, e, o(0, i)) : t[e] = i
        }
    },
    1154: function(t, e, i) {
        "use strict";
        var n = i(54)
          , o = i(32)
          , a = i(138)
          , s = i(364)
          , r = i(363)
          , l = i(141)
          , c = i(1152)
          , d = i(356);
        o(o.S + o.F * !i(365)(function(t) {
            Array.from(t)
        }), "Array", {
            from: function(t) {
                var e, i, o, u, h = a(t), p = "function" == typeof this ? this : Array, g = arguments.length, f = g > 1 ? arguments[1] : void 0, m = void 0 !== f, x = 0, v = d(h);
                if (m && (f = n(f, g > 2 ? arguments[2] : void 0, 2)),
                void 0 == v || p == Array && r(v))
                    for (e = l(h.length),
                    i = new p(e); e > x; x++)
                        c(i, x, m ? f(h[x], x) : h[x]);
                else
                    for (u = v.call(h),
                    i = new p; !(o = u.next()).done; x++)
                        c(i, x, m ? s(u, f, [o.value, x], !0) : o.value);
                return i.length = x,
                i
            }
        })
    },
    1607: function(t, e, i) {
        "use strict";
        Object.defineProperty(e, "__esModule", {
            value: !0
        });
        var n = i(1091)
          , o = i.n(n)
          , a = i(207)
          , s = i.n(a)
          , r = i(78)
          , l = i(79)
          , c = i.n(l)
          , d = i(971)
          , u = (i.n(d),
        i(962))
          , h = (i.n(u),
        i(972))
          , p = (i.n(h),
        i(976))
          , g = (i.n(p),
        i(984));
        i.n(g);
        e.default = {
            name: "FlowStatisticsPage",
            data: function() {
                return {
                    cut: "mac",
                    tableOptions: {
                        clickToEdit: !1,
                        rowEditFormat: "disabled",
                        tableClass: "table table_w checkbox_checked",
                        tableOperation: [{
                            type: "exportFile",
                            disable: !1
                        }, {
                            type: "customButton",
                            label: "log.systemLog.cleanAll",
                            emitEvent: "cleanAll",
                            disable: !1
                        }],
                        customMethods: {},
                        pagination: {
                            paginateable: !0
                        },
                        requests: {
                            param: {
                                GROUP_BY: "mac",
                                ORDER_BY: "daytime",
                                ORDER: "desc",
                                TYPE: "client_data,client_total"
                            },
                            url: r.a.apiUrl,
                            funcName: "audit_terminal_stat",
                            listAction: "show",
                            returnFieldAlias: {
                                data: "client_data",
                                total: "client_total"
                            }
                        },
                        fixColumns: ["id", "buttons", "checkbox", "enabled"],
                        columns: [{
                            name: "mac",
                            display: "text",
                            headerLabel: "behavior.flow-statistics.header_title.mac",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "comment",
                            display: "text",
                            headerLabel: "behavior.flow-statistics.header_title.comment",
                            validate: {
                                reg: "required|strLenBetween:0,64"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "buttons",
                            headerLabel: "behavior.flow-statistics.header_title.statistical_details",
                            display: "buttons",
                            cls: {
                                headerClass: "w110",
                                cellClass: "td_opear"
                            },
                            buttonsList: [{
                                type: "customButton",
                                disable: !1,
                                label: "behavior.flow-statistics.header_title.detail",
                                emitEvent: "detail"
                            }]
                        }]
                    },
                    tableOptions1: {
                        clickToEdit: !1,
                        rowEditFormat: "disabled",
                        tableClass: "table table_w checkbox_checked",
                        tableOperation: [{
                            type: "exportFile",
                            disable: !1
                        }, {
                            type: "customButton",
                            label: "log.systemLog.cleanAll",
                            emitEvent: "cleanAll",
                            disable: !1
                        }],
                        customMethods: {},
                        pagination: {
                            paginateable: !0
                        },
                        requests: {
                            param: {
                                GROUP_BY: "mac",
                                ORDER_BY: "daytime",
                                ORDER: "desc",
                                TYPE: "vpn_client_total,vpn_client_data"
                            },
                            url: r.a.apiUrl,
                            funcName: "audit_terminal_stat",
                            listAction: "show",
                            export: "EXPORT_EXTEND",
                            returnFieldAlias: {
                                data: "vpn_client_data",
                                total: "vpn_client_total"
                            }
                        },
                        fixColumns: ["id", "buttons", "checkbox", "enabled"],
                        columns: [{
                            name: "mac",
                            display: "text",
                            headerLabel: "behavior.flow-statistics.header_title.account",
                            validate: {
                                reg: "required"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "comment",
                            display: "text",
                            headerLabel: "behavior.flow-statistics.header_title.comment",
                            validate: {
                                reg: "required|strLenBetween:0,64"
                            },
                            cls: {
                                headerClass: "",
                                cellClass: ""
                            },
                            addDefault: ""
                        }, {
                            name: "buttons",
                            headerLabel: "behavior.flow-statistics.header_title.statistical_details",
                            display: "buttons",
                            cls: {
                                headerClass: "w110",
                                cellClass: "td_opear"
                            },
                            buttonsList: [{
                                type: "customButton",
                                disable: !1,
                                label: "behavior.flow-statistics.header_title.detail",
                                emitEvent: "detail"
                            }]
                        }]
                    },
                    searchText: "",
                    isShowDetail: !1,
                    ipv4UpData: [],
                    ipv4DownData: [],
                    ipv6UpData: [],
                    ipv6DownData: [],
                    MAC: "",
                    remark: "",
                    chartLoading: !1,
                    Option: {
                        color: ["#fe6f73", "#5ab1ef", "#E5CF0A", "#A086D3", "#dc69aa", "#d87a80", "#ffb980", "#e5cf0d", "#9a7fd1", "#b6a2de", "#8d98b3"],
                        calculable: !1,
                        tooltip: {
                            trigger: "axis",
                            formatter: function(t) {
                                var e = "<p>" + s()(1e3 * t[0].axisValue).format("YYYY-MM-DD") + "</p>";
                                return t.forEach(function(t) {
                                    e += "<p>" + t.marker + t.seriesName + "：" + c.a.formatBytes(t.value) + "</p>"
                                }),
                                e
                            },
                            padding: 10
                        },
                        grid: {
                            icon: "rect",
                            borderWidth: 0,
                            x: 100,
                            y: 60,
                            x2: 50,
                            y2: 60
                        },
                        legend: {
                            type: "plain",
                            x: "center",
                            y: "bottom",
                            show: !0,
                            data: []
                        },
                        xAxis: {
                            splitLine: {
                                show: !1
                            },
                            axisTick: {
                                show: !0
                            },
                            axisLine: {
                                lineStyle: {
                                    width: 1,
                                    color: "#777"
                                }
                            },
                            type: "category",
                            axisLabel: {
                                interval: 0,
                                formatter: function(t) {
                                    var e = 1e3 * t
                                      , i = new Date(e);
                                    return String(i.getMonth() + 1).padStart(2, "0") + "-" + String(i.getDate()).padStart(2, "0")
                                }
                            }
                        },
                        yAxis: {
                            name: this.$t("behavior.flow-statistics.flowStatistics"),
                            nameTextStyle: {
                                fontSize: 18
                            },
                            axisTick: {
                                show: !1
                            },
                            axisLine: {
                                onZero: !1,
                                lineStyle: {
                                    width: 1,
                                    color: "#777"
                                }
                            },
                            min: 0,
                            axisLabel: {
                                formatter: function() {
                                    return c.a.formatBytes(arguments[0])
                                }
                            },
                            type: "value"
                        },
                        series: []
                    },
                    xEnterprise: 1,
                    oemSign: 0
                }
            },
            created: function() {
                var t = this;
                getHeaders(function() {
                    t.xEnterprise = 1,
                    t.oemSign = headers.oemSign
                })
            },
            methods: {
                changeTab: function(t, e) {
                    var i = this;
                    this.cut = t,
                    this.searchText = "",
                    this.tableOptions.requests.param.KEYWORDS = this.searchText ? this.searchText : "",
                    this.tableOptions1.requests.param.KEYWORDS = this.searchText ? this.searchText : "",
                    this.$nextTick(function() {
                        i.$refs[e].reload()
                    })
                },
                search: function(t) {
                    "mac" == this.cut ? (this.tableOptions.requests.param.FINDS = "mac,comment",
                    this.tableOptions.requests.param.KEYWORDS = this.searchText ? this.searchText : "") : (this.tableOptions1.requests.param.FINDS = "mac,comment",
                    this.tableOptions1.requests.param.KEYWORDS = this.searchText ? this.searchText : ""),
                    this.$refs[t].search()
                },
                detail: function(t) {
                    var e = this
                      , i = t.row;
                    this.MAC = i.mac,
                    this.remark = i.comment,
                    this.isShowDetail = !0,
                    this.ipv4UpData = [],
                    this.ipv4DownData = [],
                    this.ipv6UpData = [],
                    this.ipv6DownData = [],
                    this.Option.series = [],
                    this.chartLoading = !0;
                    var n = {
                        GROUP_BY: "daytime",
                        ORDER_BY: "daytime",
                        ORDER: "asc",
                        TYPE: "mac" == this.cut ? "daytime,daytime6" : "daytime_vpn"
                    };
                    "mac" == this.cut ? (n.FINDS = "mac",
                    n.KEYWORDS = i.mac) : n.FILTER1 = "mac,=," + i.mac,
                    this.$http.post(r.a.apiUrl, {
                        func_name: "audit_terminal_stat",
                        action: "show",
                        param: n
                    }).then(function(t) {
                        e.Option.xAxis.data = e.getTimestamps(),
                        e.Option.legend.data = [e.$t("behavior.flow-statistics.ipv4UpFlow"), e.$t("behavior.flow-statistics.ipv4DownFlow")],
                        e.ipv4UpData = o()({
                            length: 30
                        }, function() {
                            return 0
                        }),
                        e.ipv4DownData = o()({
                            length: 30
                        }, function() {
                            return 0
                        }),
                        "mac" == e.cut && (e.ipv6UpData = o()({
                            length: 30
                        }, function() {
                            return 0
                        }),
                        e.ipv6DownData = o()({
                            length: 30
                        }, function() {
                            return 0
                        })),
                        t.data.Data["mac" == e.cut ? "daytime" : "daytime_vpn"].forEach(function(t) {
                            var i = e.Option.xAxis.data.indexOf(t.daytime);
                            e.ipv4UpData[i] = t.sum_total_up,
                            e.ipv4DownData[i] = t.sum_total_down
                        }),
                        "mac" == e.cut && t.data.Data.daytime6.forEach(function(t) {
                            var i = e.Option.xAxis.data.indexOf(t.daytime);
                            e.ipv6UpData[i] = t.sum_total_up,
                            e.ipv6DownData[i] = t.sum_total_down
                        }),
                        e.Option.series = [{
                            name: e.$t("behavior.flow-statistics.ipv4UpFlow"),
                            data: e.ipv4UpData,
                            type: "line",
                            smooth: !0,
                            symbol: "emptyCircle",
                            symbolSize: 2,
                            showSymbol: !1,
                            lineStyle: {
                                normal: {
                                    width: 2
                                }
                            }
                        }, {
                            name: e.$t("behavior.flow-statistics.ipv4DownFlow"),
                            data: e.ipv4DownData,
                            type: "line",
                            smooth: !0,
                            symbol: "emptyCircle",
                            symbolSize: 2,
                            showSymbol: !1,
                            lineStyle: {
                                normal: {
                                    width: 2
                                }
                            }
                        }],
                        "mac" == e.cut && (e.Option.legend.data.push(e.$t("behavior.flow-statistics.ipv6UpFlow"), e.$t("behavior.flow-statistics.ipv6DownFlow")),
                        e.Option.series.push({
                            name: e.$t("behavior.flow-statistics.ipv6UpFlow"),
                            data: e.ipv6UpData,
                            type: "line",
                            smooth: !0,
                            symbol: "emptyCircle",
                            symbolSize: 2,
                            showSymbol: !1,
                            lineStyle: {
                                normal: {
                                    width: 2
                                }
                            }
                        }, {
                            name: e.$t("behavior.flow-statistics.ipv6DownFlow"),
                            data: e.ipv6DownData,
                            type: "line",
                            smooth: !0,
                            symbol: "emptyCircle",
                            symbolSize: 2,
                            showSymbol: !1,
                            lineStyle: {
                                normal: {
                                    width: 2
                                }
                            }
                        })),
                        e.chartLoading = !1
                    })
                },
                closeDetail: function() {
                    this.isShowDetail = !1
                },
                getTimestamps: function() {
                    var t = []
                      , e = new Date;
                    e.setHours(0, 0, 0, 0);
                    for (var i = 0; i < 30; i++) {
                        var n = e.getTime() - 24 * i * 60 * 60 * 1e3;
                        t.push(Math.floor(n / 1e3))
                    }
                    return t.sort(function(t, e) {
                        return t - e
                    })
                },
                cleanAll: function(t) {
                    var e = this;
                    customConfirm(this.$t("behavior.flow-statistics.cleanTip")).then(function(i) {
                        e.$http.post(r.a.apiUrl, {
                            func_name: "audit_terminal_stat",
                            action: "clean"
                        }).then(function() {
                            customSuccess(e.$t("common.operationSuccess")),
                            e.$nextTick(function() {
                                e.$refs[t].reload()
                            })
                        })
                    })
                }
            }
        }
    },
    2344: function(t, e) {
        t.exports = {
            render: function() {
                var t = this
                  , e = t.$createElement
                  , i = t._self._c || e;
                return i("div", [t.isShowDetail || !t.xEnterprise && 2 != t.oemSign ? t.isShowDetail && (t.xEnterprise || 2 == t.oemSign) ? i("div", {
                    staticClass: "main_section_edit"
                }, [i("div", {
                    staticClass: "title_h3 clearfix"
                }, [i("h3", [t._v(t._s(t.$t("behavior.flow-statistics.header_title.detail")) + " "), i("span", {
                    directives: [{
                        name: "show",
                        rawName: "v-show",
                        value: t.remark,
                        expression: "remark"
                    }]
                }, [t._v("-" + t._s(t.remark))]), t._v(" (" + t._s(t.MAC) + ")")]), t._v(" "), i("div", {
                    staticClass: "helpService"
                }, [i("a", {
                    staticClass: "close_edit close_ico",
                    attrs: {
                        href: "javascript:void(0)"
                    },
                    on: {
                        click: t.closeDetail
                    }
                }, [t._v("×")])])]), t._v(" "), i("div", {
                    staticClass: "wrapper clearfix row"
                }, [i("div", {
                    staticClass: "box clearfix"
                }, [i("div", {
                    staticClass: "h10"
                }), t._v(" "), i("div", {
                    staticClass: "box_block"
                }, [i("div", {
                    staticStyle: {
                        height: "300px",
                        margin: "0 auto"
                    }
                }, [i("IEcharts", {
                    ref: "myEchart",
                    attrs: {
                        resizable: !0,
                        option: t.Option,
                        loading: t.chartLoading
                    }
                })], 1)])])])]) : i("div", {
                    staticClass: "qaq3"
                }, [i("div", {
                    staticClass: "main_section"
                }, [i("sub-title-section", {
                    attrs: {
                        opturl: {
                            helpUrl: "id=112&Itemid=200"
                        },
                        opt: {
                            helpMessage: t.$t("helpTip.protocolTip")
                        }
                    }
                }), t._v(" "), i("div", {
                    staticStyle: {
                        width: "100%",
                        "text-align": "center",
                        "line-height": "150%",
                        "margin-top": "20%",
                        "font-size": "14px"
                    }
                }, [i("i", {
                    staticClass: "ico-mark"
                }), t._v(t._s(t.$t("common.xEnterprise_2")) + "\n      ")])], 1)]) : i("div", {
                    staticClass: "qaq3"
                }, [i("sub-title-section", {
                    attrs: {
                        opturl: {
                            helpUrl: "id=1493&Itemid=2111"
                        },
                        opt: {
                            helpMessage: t.$t("helpTip.terminalTrafficStatisticsTip")
                        }
                    }
                }), t._v(" "), i("div", {
                    staticClass: "wrapper row"
                }, [i("div", {
                    staticClass: "box clearfix"
                }, [i("div", {
                    staticClass: "clearfix",
                    staticStyle: {
                        "margin-bottom": "20px"
                    }
                }, [i("div", {
                    staticClass: "menu seitchHF_radio"
                }, [i("label", {
                    staticClass: "radio_hidden",
                    class: {
                        active: "mac" == t.cut
                    }
                }, [i("input", {
                    attrs: {
                        name: "dc1",
                        checked: "checked",
                        type: "radio"
                    },
                    on: {
                        click: function(e) {
                            t.changeTab("mac", "dtable")
                        }
                    }
                }), t._v("MAC\n            ")]), t._v(" "), i("label", {
                    staticClass: "radio_hidden radio_l_border",
                    class: {
                        active: "account" == t.cut
                    }
                }, [i("input", {
                    attrs: {
                        name: "dc1",
                        type: "radio"
                    },
                    on: {
                        click: function(e) {
                            t.changeTab("account", "dtable1")
                        }
                    }
                }), t._v(t._s(t.$t("behavior.flow-statistics.header_title.account")) + "\n            ")])])]), t._v(" "), "mac" == t.cut ? i("d-table", {
                    ref: "dtable",
                    attrs: {
                        opt: t.tableOptions
                    },
                    on: {
                        detail: t.detail,
                        cleanAll: function(e) {
                            t.cleanAll("dtable")
                        }
                    }
                }, [i("div", {
                    staticClass: "fl table_refresh",
                    slot: "searchArea"
                }, [i("div", {
                    staticClass: "search_list",
                    staticStyle: {
                        "min-width": "180px"
                    }
                }, [i("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: t.searchText,
                        expression: "searchText"
                    }],
                    staticClass: "focuseText inptText search_inpt",
                    attrs: {
                        placeholder: "MAC/" + t.$t("common.comment"),
                        type: "text"
                    },
                    domProps: {
                        value: t.searchText
                    },
                    on: {
                        change: function(e) {
                            t.search("dtable")
                        },
                        input: function(e) {
                            e.target.composing || (t.searchText = e.target.value)
                        }
                    }
                }), t._v(" "), i("input", {
                    staticClass: "search_icon",
                    attrs: {
                        type: "button"
                    }
                })])])]) : "account" == t.cut ? i("d-table", {
                    ref: "dtable1",
                    attrs: {
                        opt: t.tableOptions1
                    },
                    on: {
                        detail: t.detail,
                        cleanAll: function(e) {
                            t.cleanAll("dtable1")
                        }
                    }
                }, [i("div", {
                    staticClass: "fl table_refresh",
                    slot: "searchArea"
                }, [i("div", {
                    staticClass: "search_list",
                    staticStyle: {
                        "min-width": "180px"
                    }
                }, [i("input", {
                    directives: [{
                        name: "model",
                        rawName: "v-model",
                        value: t.searchText,
                        expression: "searchText"
                    }],
                    staticClass: "focuseText inptText search_inpt",
                    attrs: {
                        placeholder: t.$t("behavior.flow-statistics.header_title.account") + "/" + t.$t("common.comment"),
                        type: "text"
                    },
                    domProps: {
                        value: t.searchText
                    },
                    on: {
                        change: function(e) {
                            t.search("dtable1")
                        },
                        input: function(e) {
                            e.target.composing || (t.searchText = e.target.value)
                        }
                    }
                }), t._v(" "), i("input", {
                    staticClass: "search_icon",
                    attrs: {
                        type: "button"
                    }
                })])])]) : t._e()], 1)])], 1)])
            },
            staticRenderFns: []
        }
    },
    794: function(t, e, i) {
        var n = i(23)(i(1607), i(2344), null, null);
        t.exports = n.exports
    },
    936: function(t, e, i) {
        function n(t, e) {
            var i = {
                axesInfo: {},
                seriesInvolved: !1,
                coordSysAxesInfo: {},
                coordSysMap: {}
            };
            return o(i, t, e),
            i.seriesInvolved && s(i, t),
            i
        }
        function o(t, e, i) {
            var n = e.getComponent("tooltip")
              , o = e.getComponent("axisPointer")
              , s = o.get("link", !0) || []
              , l = [];
            m(i.getCoordinateSystems(), function(i) {
                function c(n, c, d) {
                    var g = d.model.getModel("axisPointer", o)
                      , m = g.get("show");
                    if (m && ("auto" !== m || n || h(g))) {
                        null == c && (c = g.get("triggerTooltip")),
                        g = n ? a(d, f, o, e, n, c) : g;
                        var x = g.get("snap")
                          , v = p(d.model)
                          , y = c || x || "category" === d.type
                          , _ = t.axesInfo[v] = {
                            key: v,
                            axis: d,
                            coordSys: i,
                            axisPointerModel: g,
                            triggerTooltip: c,
                            involveSeries: y,
                            snap: x,
                            useHandle: h(g),
                            seriesModels: []
                        };
                        u[v] = _,
                        t.seriesInvolved |= y;
                        var b = r(s, d);
                        if (null != b) {
                            var w = l[b] || (l[b] = {
                                axesInfo: {}
                            });
                            w.axesInfo[v] = _,
                            w.mapper = s[b].mapper,
                            _.linkGroup = w
                        }
                    }
                }
                if (i.axisPointerEnabled) {
                    var d = p(i.model)
                      , u = t.coordSysAxesInfo[d] = {};
                    t.coordSysMap[d] = i;
                    var g = i.model
                      , f = g.getModel("tooltip", n);
                    if (m(i.getAxes(), x(c, !1, null)),
                    i.getTooltipAxes && n && f.get("show")) {
                        var v = "axis" === f.get("trigger")
                          , y = "cross" === f.get("axisPointer.type")
                          , _ = i.getTooltipAxes(f.get("axisPointer.axis"));
                        (v || y) && m(_.baseAxes, x(c, !y || "cross", v)),
                        y && m(_.otherAxes, x(c, "cross", !1))
                    }
                }
            })
        }
        function a(t, e, i, n, o, a) {
            var s = e.getModel("axisPointer")
              , r = {};
            m(["type", "snap", "lineStyle", "shadowStyle", "label", "animation", "animationDurationUpdate", "animationEasingUpdate", "z"], function(t) {
                r[t] = g.clone(s.get(t))
            }),
            r.snap = "category" !== t.type && !!a,
            "cross" === s.get("type") && (r.type = "line");
            var l = r.label || (r.label = {});
            if (null == l.show && (l.show = !1),
            "cross" === o) {
                var c = s.get("label.show");
                if (l.show = null == c || c,
                !a) {
                    var d = r.lineStyle = s.get("crossStyle");
                    d && g.defaults(l, d.textStyle)
                }
            }
            return t.model.getModel("axisPointer", new f(r,i,n))
        }
        function s(t, e) {
            e.eachSeries(function(e) {
                var i = e.coordinateSystem
                  , n = e.get("tooltip.trigger", !0)
                  , o = e.get("tooltip.show", !0);
                i && "none" !== n && !1 !== n && "item" !== n && !1 !== o && !1 !== e.get("axisPointer.show", !0) && m(t.coordSysAxesInfo[p(i.model)], function(t) {
                    var n = t.axis;
                    i.getAxis(n.dim) === n && (t.seriesModels.push(e),
                    null == t.seriesDataCount && (t.seriesDataCount = 0),
                    t.seriesDataCount += e.getData().count())
                })
            }, this)
        }
        function r(t, e) {
            for (var i = e.model, n = e.dim, o = 0; o < t.length; o++) {
                var a = t[o] || {};
                if (l(a[n + "AxisId"], i.id) || l(a[n + "AxisIndex"], i.componentIndex) || l(a[n + "AxisName"], i.name))
                    return o
            }
        }
        function l(t, e) {
            return "all" === t || g.isArray(t) && g.indexOf(t, e) >= 0 || t === e
        }
        function c(t) {
            var e = d(t);
            if (e) {
                var i = e.axisPointerModel
                  , n = e.axis.scale
                  , o = i.option
                  , a = i.get("status")
                  , s = i.get("value");
                null != s && (s = n.parse(s));
                var r = h(i);
                null == a && (o.status = r ? "show" : "hide");
                var l = n.getExtent().slice();
                l[0] > l[1] && l.reverse(),
                (null == s || s > l[1]) && (s = l[1]),
                s < l[0] && (s = l[0]),
                o.value = s,
                r && (o.status = e.axis.scale.isBlank() ? "hide" : "show")
            }
        }
        function d(t) {
            var e = (t.ecModel.getComponent("axisPointer") || {}).coordSysAxesInfo;
            return e && e.axesInfo[p(t)]
        }
        function u(t) {
            var e = d(t);
            return e && e.axisPointerModel
        }
        function h(t) {
            return !!t.get("handle.show")
        }
        function p(t) {
            return t.type + "||" + t.id
        }
        var g = i(1)
          , f = i(82)
          , m = g.each
          , x = g.curry;
        e.collect = n,
        e.fixValue = c,
        e.getAxisInfo = d,
        e.getAxisPointerModel = u,
        e.makeKey = p
    },
    938: function(t, e, i) {
        function n(t) {
            var e = {
                componentType: t.mainType,
                componentIndex: t.componentIndex
            };
            return e[t.mainType + "Index"] = t.componentIndex,
            e
        }
        function o(t, e, i, n) {
            var o, a, s = w(i - t.rotation), r = n[0] > n[1], l = "start" === e && !r || "start" !== e && r;
            return b(s - O / 2) ? (a = l ? "bottom" : "top",
            o = "center") : b(s - 1.5 * O) ? (a = l ? "top" : "bottom",
            o = "center") : (a = "middle",
            o = s < 1.5 * O && s > O / 2 ? l ? "left" : "right" : l ? "right" : "left"),
            {
                rotation: s,
                textAlign: o,
                textVerticalAlign: a
            }
        }
        function a(t) {
            var e = t.get("tooltip");
            return t.get("silent") || !(t.get("triggerEvent") || e && e.show)
        }
        function s(t, e, i) {
            if (!M(t.axis)) {
                var n = t.get("axisLabel.showMinLabel")
                  , o = t.get("axisLabel.showMaxLabel");
                e = e || [],
                i = i || [];
                var a = e[0]
                  , s = e[1]
                  , c = e[e.length - 1]
                  , d = e[e.length - 2]
                  , u = i[0]
                  , h = i[1]
                  , p = i[i.length - 1]
                  , g = i[i.length - 2];
                !1 === n ? (r(a),
                r(u)) : l(a, s) && (n ? (r(s),
                r(h)) : (r(a),
                r(u))),
                !1 === o ? (r(c),
                r(p)) : l(d, c) && (o ? (r(d),
                r(g)) : (r(c),
                r(p)))
            }
        }
        function r(t) {
            t && (t.ignore = !0)
        }
        function l(t, e, i) {
            var n = t && t.getBoundingRect().clone()
              , o = e && e.getBoundingRect().clone();
            if (n && o) {
                var a = C.identity([]);
                return C.rotate(a, a, -t.rotation),
                n.applyTransform(C.mul([], a, t.getLocalTransform())),
                o.applyTransform(C.mul([], a, e.getLocalTransform())),
                n.intersect(o)
            }
        }
        function c(t) {
            return "middle" === t || "center" === t
        }
        function d(t, e, i) {
            var n = e.axis;
            if (e.get("axisTick.show") && !n.scale.isBlank()) {
                for (var o = e.getModel("axisTick"), a = o.getModel("lineStyle"), s = o.get("length"), r = n.getTicksCoords(), l = [], c = [], d = t._transform, u = [], h = 0; h < r.length; h++) {
                    var p = r[h].coord;
                    l[0] = p,
                    l[1] = 0,
                    c[0] = p,
                    c[1] = i.tickDirection * s,
                    d && (I(l, l, d),
                    I(c, c, d));
                    var f = new v.Line(v.subPixelOptimizeLine({
                        anid: "tick_" + r[h].tickValue,
                        shape: {
                            x1: l[0],
                            y1: l[1],
                            x2: c[0],
                            y2: c[1]
                        },
                        style: g(a.getLineStyle(), {
                            stroke: e.get("axisLine.lineStyle.color")
                        }),
                        z2: 2,
                        silent: !0
                    }));
                    t.group.add(f),
                    u.push(f)
                }
                return u
            }
        }
        function u(t, e, i) {
            var o = e.axis;
            if (p(i.axisLabelShow, e.get("axisLabel.show")) && !o.scale.isBlank()) {
                var s = e.getModel("axisLabel")
                  , r = s.get("margin")
                  , l = o.getViewLabels()
                  , c = (p(i.labelRotate, s.get("rotate")) || 0) * O / 180
                  , d = L(i.rotation, c, i.labelDirection)
                  , u = e.getCategories(!0)
                  , h = []
                  , g = a(e)
                  , f = e.get("triggerEvent");
                return m(l, function(a, l) {
                    var c = a.tickValue
                      , p = a.formattedLabel
                      , m = a.rawLabel
                      , x = s;
                    u && u[c] && u[c].textStyle && (x = new y(u[c].textStyle,s,e.ecModel));
                    var _ = x.getTextColor() || e.get("axisLine.lineStyle.color")
                      , b = o.dataToCoord(c)
                      , w = [b, i.labelOffset + i.labelDirection * r]
                      , S = new v.Text({
                        anid: "label_" + c,
                        position: w,
                        rotation: d.rotation,
                        silent: g,
                        z2: 10
                    });
                    v.setTextStyle(S.style, x, {
                        text: p,
                        textAlign: x.getShallow("align", !0) || d.textAlign,
                        textVerticalAlign: x.getShallow("verticalAlign", !0) || x.getShallow("baseline", !0) || d.textVerticalAlign,
                        textFill: "function" == typeof _ ? _("category" === o.type ? m : "value" === o.type ? c + "" : c, l) : _
                    }),
                    f && (S.eventData = n(e),
                    S.eventData.targetType = "axisLabel",
                    S.eventData.value = m),
                    t._dumbGroup.add(S),
                    S.updateTransform(),
                    h.push(S),
                    t.group.add(S),
                    S.decomposeTransform()
                }),
                h
            }
        }
        var h = i(1)
          , p = h.retrieve
          , g = h.defaults
          , f = h.extend
          , m = h.each
          , x = i(68)
          , v = i(77)
          , y = i(82)
          , _ = i(30)
          , b = _.isRadianAroundZero
          , w = _.remRadian
          , S = i(345)
          , A = S.createSymbol
          , C = i(83)
          , T = i(17)
          , I = T.applyTransform
          , D = i(206)
          , M = D.shouldShowAllLabels
          , O = Math.PI
          , P = function(t, e) {
            this.opt = e,
            this.axisModel = t,
            g(e, {
                labelOffset: 0,
                nameDirection: 1,
                tickDirection: 1,
                labelDirection: 1,
                silent: !0
            }),
            this.group = new v.Group;
            var i = new v.Group({
                position: e.position.slice(),
                rotation: e.rotation
            });
            i.updateTransform(),
            this._transform = i.transform,
            this._dumbGroup = i
        };
        P.prototype = {
            constructor: P,
            hasBuilder: function(t) {
                return !!k[t]
            },
            add: function(t) {
                k[t].call(this)
            },
            getGroup: function() {
                return this.group
            }
        };
        var k = {
            axisLine: function() {
                var t = this.opt
                  , e = this.axisModel;
                if (e.get("axisLine.show")) {
                    var i = this.axisModel.axis.getExtent()
                      , n = this._transform
                      , o = [i[0], 0]
                      , a = [i[1], 0];
                    n && (I(o, o, n),
                    I(a, a, n));
                    var s = f({
                        lineCap: "round"
                    }, e.getModel("axisLine.lineStyle").getLineStyle());
                    this.group.add(new v.Line(v.subPixelOptimizeLine({
                        anid: "line",
                        shape: {
                            x1: o[0],
                            y1: o[1],
                            x2: a[0],
                            y2: a[1]
                        },
                        style: s,
                        strokeContainThreshold: t.strokeContainThreshold || 5,
                        silent: !0,
                        z2: 1
                    })));
                    var r = e.get("axisLine.symbol")
                      , l = e.get("axisLine.symbolSize")
                      , c = e.get("axisLine.symbolOffset") || 0;
                    if ("number" == typeof c && (c = [c, c]),
                    null != r) {
                        "string" == typeof r && (r = [r, r]),
                        "string" != typeof l && "number" != typeof l || (l = [l, l]);
                        var d = l[0]
                          , u = l[1];
                        m([{
                            rotate: t.rotation + Math.PI / 2,
                            offset: c[0],
                            r: 0
                        }, {
                            rotate: t.rotation - Math.PI / 2,
                            offset: c[1],
                            r: Math.sqrt((o[0] - a[0]) * (o[0] - a[0]) + (o[1] - a[1]) * (o[1] - a[1]))
                        }], function(e, i) {
                            if ("none" !== r[i] && null != r[i]) {
                                var n = A(r[i], -d / 2, -u / 2, d, u, s.stroke, !0)
                                  , a = e.r + e.offset
                                  , l = [o[0] + a * Math.cos(t.rotation), o[1] - a * Math.sin(t.rotation)];
                                n.attr({
                                    rotation: e.rotate,
                                    position: l,
                                    silent: !0,
                                    z2: 11
                                }),
                                this.group.add(n)
                            }
                        }, this)
                    }
                }
            },
            axisTickLabel: function() {
                var t = this.axisModel
                  , e = this.opt
                  , i = d(this, t, e);
                s(t, u(this, t, e), i)
            },
            axisName: function() {
                var t = this.opt
                  , e = this.axisModel
                  , i = p(t.axisName, e.get("name"));
                if (i) {
                    var s, r = e.get("nameLocation"), l = t.nameDirection, d = e.getModel("nameTextStyle"), u = e.get("nameGap") || 0, h = this.axisModel.axis.getExtent(), g = h[0] > h[1] ? -1 : 1, m = ["start" === r ? h[0] - g * u : "end" === r ? h[1] + g * u : (h[0] + h[1]) / 2, c(r) ? t.labelOffset + l * u : 0], y = e.get("nameRotate");
                    null != y && (y = y * O / 180);
                    var _;
                    c(r) ? s = L(t.rotation, null != y ? y : t.rotation, l) : (s = o(t, r, y || 0, h),
                    null != (_ = t.axisNameAvailableWidth) && (_ = Math.abs(_ / Math.sin(s.rotation)),
                    !isFinite(_) && (_ = null)));
                    var b = d.getFont()
                      , w = e.get("nameTruncate", !0) || {}
                      , S = w.ellipsis
                      , A = p(t.nameTruncateMaxWidth, w.maxWidth, _)
                      , C = null != S && null != A ? x.truncateText(i, A, b, S, {
                        minChar: 2,
                        placeholder: w.placeholder
                    }) : i
                      , T = e.get("tooltip", !0)
                      , I = e.mainType
                      , D = {
                        componentType: I,
                        name: i,
                        $vars: ["name"]
                    };
                    D[I + "Index"] = e.componentIndex;
                    var M = new v.Text({
                        anid: "name",
                        __fullText: i,
                        __truncatedText: C,
                        position: m,
                        rotation: s.rotation,
                        silent: a(e),
                        z2: 1,
                        tooltip: T && T.show ? f({
                            content: i,
                            formatter: function() {
                                return i
                            },
                            formatterParams: D
                        }, T) : null
                    });
                    v.setTextStyle(M.style, d, {
                        text: C,
                        textFont: b,
                        textFill: d.getTextColor() || e.get("axisLine.lineStyle.color"),
                        textAlign: s.textAlign,
                        textVerticalAlign: s.textVerticalAlign
                    }),
                    e.get("triggerEvent") && (M.eventData = n(e),
                    M.eventData.targetType = "axisName",
                    M.eventData.name = i),
                    this._dumbGroup.add(M),
                    M.updateTransform(),
                    this.group.add(M),
                    M.decomposeTransform()
                }
            }
        }
          , L = P.innerTextLayout = function(t, e, i) {
            var n, o, a = w(e - t);
            return b(a) ? (o = i > 0 ? "top" : "bottom",
            n = "center") : b(a - O) ? (o = i > 0 ? "bottom" : "top",
            n = "center") : (o = "middle",
            n = a > 0 && a < O ? i > 0 ? "right" : "left" : i > 0 ? "left" : "right"),
            {
                rotation: a,
                textAlign: n,
                textVerticalAlign: o
            }
        }
          , E = P;
        t.exports = E
    },
    939: function(t, e, i) {
        function n(t, e, i, n, a, s) {
            var c = l.getAxisPointerClass(t.axisPointerClass);
            if (c) {
                var d = r.getAxisPointerModel(e);
                d ? (t._axisPointer || (t._axisPointer = new c)).render(e, d, n, s) : o(t, n)
            }
        }
        function o(t, e, i) {
            var n = t._axisPointer;
            n && n.dispose(e, i),
            t._axisPointer = null
        }
        var a = i(24)
          , s = (a.__DEV__,
        i(343))
          , r = i(936)
          , l = s.extendComponentView({
            type: "axis",
            _axisPointer: null,
            axisPointerClass: null,
            render: function(t, e, i, o) {
                this.axisPointerClass && r.fixValue(t),
                l.superApply(this, "render", arguments),
                n(this, t, e, i, o, !0)
            },
            updateAxisPointer: function(t, e, i, o, a) {
                n(this, t, e, i, o, !1)
            },
            remove: function(t, e) {
                var i = this._axisPointer;
                i && i.remove(e),
                l.superApply(this, "remove", arguments)
            },
            dispose: function(t, e) {
                o(this, e),
                l.superApply(this, "dispose", arguments)
            }
        })
          , c = [];
        l.registerAxisPointerClass = function(t, e) {
            c[t] = e
        }
        ,
        l.getAxisPointerClass = function(t) {
            return t && c[t]
        }
        ;
        var d = l;
        t.exports = d
    },
    942: function(t, e) {
        function i(t, e, i) {
            return {
                seriesType: t,
                performRawSeries: !0,
                reset: function(t, n, o) {
                    function a(e, i) {
                        if ("function" == typeof l) {
                            var n = t.getRawValue(i)
                              , o = t.getDataParams(i);
                            e.setItemVisual(i, "symbolSize", l(n, o))
                        }
                        if (e.hasItemOption) {
                            var a = e.getItemModel(i)
                              , s = a.getShallow("symbol", !0)
                              , r = a.getShallow("symbolSize", !0)
                              , c = a.getShallow("symbolKeepAspect", !0);
                            null != s && e.setItemVisual(i, "symbol", s),
                            null != r && e.setItemVisual(i, "symbolSize", r),
                            null != c && e.setItemVisual(i, "symbolKeepAspect", c)
                        }
                    }
                    var s = t.getData()
                      , r = t.get("symbol") || e
                      , l = t.get("symbolSize")
                      , c = t.get("symbolKeepAspect");
                    if (s.setVisual({
                        legendSymbol: i || r,
                        symbol: r,
                        symbolSize: l,
                        symbolKeepAspect: c
                    }),
                    !n.isSeriesFiltered(t)) {
                        var d = "function" == typeof l;
                        return {
                            dataEach: s.hasItemOption || d ? a : null
                        }
                    }
                }
            }
        }
        t.exports = i
    },
    944: function(t, e, i) {
        function n(t, e, i) {
            p.Group.call(this),
            this.updateData(t, e, i)
        }
        function o(t) {
            return [t[0] / 2, t[1] / 2]
        }
        function a(t, e) {
            this.parent.drift(t, e)
        }
        function s() {
            !p.isInEmphasis(this) && l.call(this)
        }
        function r() {
            !p.isInEmphasis(this) && c.call(this)
        }
        function l() {
            if (!this.incremental && !this.useHoverLayer) {
                var t = this.__symbolOriginalScale
                  , e = t[1] / t[0];
                this.animateTo({
                    scale: [Math.max(1.1 * t[0], t[0] + 3), Math.max(1.1 * t[1], t[1] + 3 * e)]
                }, 400, "elasticOut")
            }
        }
        function c() {
            this.incremental || this.useHoverLayer || this.animateTo({
                scale: this.__symbolOriginalScale
            }, 400, "elasticOut")
        }
        var d = i(1)
          , u = i(345)
          , h = u.createSymbol
          , p = i(77)
          , g = i(30)
          , f = g.parsePercent
          , m = i(961)
          , x = m.getDefaultLabel
          , v = n.prototype
          , y = n.getSymbolSize = function(t, e) {
            var i = t.getItemVisual(e, "symbolSize");
            return i instanceof Array ? i.slice() : [+i, +i]
        }
        ;
        v._createSymbol = function(t, e, i, n, s) {
            this.removeAll();
            var r = e.getItemVisual(i, "color")
              , l = h(t, -1, -1, 2, 2, r, s);
            l.attr({
                z2: 100,
                culling: !0,
                scale: o(n)
            }),
            l.drift = a,
            this._symbolType = t,
            this.add(l)
        }
        ,
        v.stopSymbolAnimation = function(t) {
            this.childAt(0).stopAnimation(t)
        }
        ,
        v.getSymbolPath = function() {
            return this.childAt(0)
        }
        ,
        v.getScale = function() {
            return this.childAt(0).scale
        }
        ,
        v.highlight = function() {
            this.childAt(0).trigger("emphasis")
        }
        ,
        v.downplay = function() {
            this.childAt(0).trigger("normal")
        }
        ,
        v.setZ = function(t, e) {
            var i = this.childAt(0);
            i.zlevel = t,
            i.z = e
        }
        ,
        v.setDraggable = function(t) {
            var e = this.childAt(0);
            e.draggable = t,
            e.cursor = t ? "move" : "pointer"
        }
        ,
        v.updateData = function(t, e, i) {
            this.silent = !1;
            var n = t.getItemVisual(e, "symbol") || "circle"
              , a = t.hostModel
              , s = y(t, e)
              , r = n !== this._symbolType;
            if (r) {
                var l = t.getItemVisual(e, "symbolKeepAspect");
                this._createSymbol(n, t, e, s, l)
            } else {
                var c = this.childAt(0);
                c.silent = !1,
                p.updateProps(c, {
                    scale: o(s)
                }, a, e)
            }
            if (this._updateCommon(t, e, s, i),
            r) {
                var c = this.childAt(0)
                  , d = i && i.fadeIn
                  , u = {
                    scale: c.scale.slice()
                };
                d && (u.style = {
                    opacity: c.style.opacity
                }),
                c.scale = [0, 0],
                d && (c.style.opacity = 0),
                p.initProps(c, u, a, e)
            }
            this._seriesModel = a
        }
        ;
        var _ = ["itemStyle"]
          , b = ["emphasis", "itemStyle"]
          , w = ["label"]
          , S = ["emphasis", "label"];
        v._updateCommon = function(t, e, i, n) {
            function a(e, i) {
                return E ? t.getName(e) : x(t, e)
            }
            var u = this.childAt(0)
              , h = t.hostModel
              , g = t.getItemVisual(e, "color");
            "image" !== u.type && u.useStyle({
                strokeNoScale: !0
            });
            var m = n && n.itemStyle
              , v = n && n.hoverItemStyle
              , y = n && n.symbolRotate
              , A = n && n.symbolOffset
              , C = n && n.labelModel
              , T = n && n.hoverLabelModel
              , I = n && n.hoverAnimation
              , D = n && n.cursorStyle;
            if (!n || t.hasItemOption) {
                var M = n && n.itemModel ? n.itemModel : t.getItemModel(e);
                m = M.getModel(_).getItemStyle(["color"]),
                v = M.getModel(b).getItemStyle(),
                y = M.getShallow("symbolRotate"),
                A = M.getShallow("symbolOffset"),
                C = M.getModel(w),
                T = M.getModel(S),
                I = M.getShallow("hoverAnimation"),
                D = M.getShallow("cursor")
            } else
                v = d.extend({}, v);
            var O = u.style;
            u.attr("rotation", (y || 0) * Math.PI / 180 || 0),
            A && u.attr("position", [f(A[0], i[0]), f(A[1], i[1])]),
            D && u.attr("cursor", D),
            u.setColor(g, n && n.symbolInnerColor),
            u.setStyle(m);
            var P = t.getItemVisual(e, "opacity");
            null != P && (O.opacity = P);
            var k = t.getItemVisual(e, "liftZ")
              , L = u.__z2Origin;
            null != k ? null == L && (u.__z2Origin = u.z2,
            u.z2 += k) : null != L && (u.z2 = L,
            u.__z2Origin = null);
            var E = n && n.useNameLabel;
            p.setLabelStyle(O, v, C, T, {
                labelFetcher: h,
                labelDataIndex: e,
                defaultText: a,
                isRectText: !0,
                autoColor: g
            }),
            u.off("mouseover").off("mouseout").off("emphasis").off("normal"),
            u.hoverStyle = v,
            p.setHoverStyle(u),
            u.__symbolOriginalScale = o(i),
            I && h.isAnimationEnabled() && u.on("mouseover", s).on("mouseout", r).on("emphasis", l).on("normal", c)
        }
        ,
        v.fadeOut = function(t, e) {
            var i = this.childAt(0);
            this.silent = i.silent = !0,
            !(e && e.keepLabel) && (i.style.text = null),
            p.updateProps(i, {
                style: {
                    opacity: 0
                },
                scale: [0, 0]
            }, this._seriesModel, this.dataIndex, t)
        }
        ,
        d.inherits(n, p.Group);
        var A = n;
        t.exports = A
    },
    945: function(t, e, i) {
        function n(t) {
            var e, i = t.get("type"), n = t.getModel(i + "Style");
            return "line" === i ? (e = n.getLineStyle(),
            e.fill = null) : "shadow" === i && (e = n.getAreaStyle(),
            e.stroke = null),
            e
        }
        function o(t, e, i, n, o) {
            var r = i.get("value")
              , l = s(r, e.axis, e.ecModel, i.get("seriesDataIndices"), {
                precision: i.get("label.precision"),
                formatter: i.get("label.formatter")
            })
              , c = i.getModel("label")
              , d = f.normalizeCssArray(c.get("padding") || 0)
              , u = c.getFont()
              , h = g.getBoundingRect(l, u)
              , p = o.position
              , m = h.width + d[1] + d[3]
              , x = h.height + d[0] + d[2]
              , v = o.align;
            "right" === v && (p[0] -= m),
            "center" === v && (p[0] -= m / 2);
            var y = o.verticalAlign;
            "bottom" === y && (p[1] -= x),
            "middle" === y && (p[1] -= x / 2),
            a(p, m, x, n);
            var _ = c.get("backgroundColor");
            _ && "auto" !== _ || (_ = e.get("axisLine.lineStyle.color")),
            t.label = {
                shape: {
                    x: 0,
                    y: 0,
                    width: m,
                    height: x,
                    r: c.get("borderRadius")
                },
                position: p.slice(),
                style: {
                    text: l,
                    textFont: u,
                    textFill: c.getTextColor(),
                    textPosition: "inside",
                    fill: _,
                    stroke: c.get("borderColor") || "transparent",
                    lineWidth: c.get("borderWidth") || 0,
                    shadowBlur: c.get("shadowBlur"),
                    shadowColor: c.get("shadowColor"),
                    shadowOffsetX: c.get("shadowOffsetX"),
                    shadowOffsetY: c.get("shadowOffsetY")
                },
                z2: 10
            }
        }
        function a(t, e, i, n) {
            var o = n.getWidth()
              , a = n.getHeight();
            t[0] = Math.min(t[0] + e, o) - e,
            t[1] = Math.min(t[1] + i, a) - i,
            t[0] = Math.max(t[0], 0),
            t[1] = Math.max(t[1], 0)
        }
        function s(t, e, i, n, o) {
            t = e.scale.parse(t);
            var a = e.scale.getLabel(t, {
                precision: o.precision
            })
              , s = o.formatter;
            if (s) {
                var r = {
                    value: x.getAxisRawValue(e, t),
                    seriesData: []
                };
                h.each(n, function(t) {
                    var e = i.getSeriesByIndex(t.seriesIndex)
                      , n = t.dataIndexInside
                      , o = e && e.getDataParams(n);
                    o && r.seriesData.push(o)
                }),
                h.isString(s) ? a = s.replace("{value}", a) : h.isFunction(s) && (a = s(r))
            }
            return a
        }
        function r(t, e, i) {
            var n = m.create();
            return m.rotate(n, n, i.rotation),
            m.translate(n, n, i.position),
            p.applyTransform([t.dataToCoord(e), (i.labelOffset || 0) + (i.labelDirection || 1) * (i.labelMargin || 0)], n)
        }
        function l(t, e, i, n, a, s) {
            var l = v.innerTextLayout(i.rotation, 0, i.labelDirection);
            i.labelMargin = a.get("label.margin"),
            o(e, n, a, s, {
                position: r(n.axis, t, i),
                align: l.textAlign,
                verticalAlign: l.textVerticalAlign
            })
        }
        function c(t, e, i) {
            return i = i || 0,
            {
                x1: t[i],
                y1: t[1 - i],
                x2: e[i],
                y2: e[1 - i]
            }
        }
        function d(t, e, i) {
            return i = i || 0,
            {
                x: t[i],
                y: t[1 - i],
                width: e[i],
                height: e[1 - i]
            }
        }
        function u(t, e, i, n, o, a) {
            return {
                cx: t,
                cy: e,
                r0: i,
                r: n,
                startAngle: o,
                endAngle: a,
                clockwise: !0
            }
        }
        var h = i(1)
          , p = i(77)
          , g = i(84)
          , f = i(68)
          , m = i(83)
          , x = i(206)
          , v = i(938);
        e.buildElStyle = n,
        e.buildLabelElOption = o,
        e.getValueLabel = s,
        e.getTransformedPosition = r,
        e.buildCartesianSingleLabelElOption = l,
        e.makeLineShape = c,
        e.makeRectShape = d,
        e.makeSectorShape = u
    },
    946: function(t, e, i) {
        var n = i(343)
          , o = i(1)
          , a = i(77);
        i(960),
        i(995),
        n.extendComponentView({
            type: "grid",
            render: function(t, e) {
                this.group.removeAll(),
                t.get("show") && this.group.add(new a.Rect({
                    shape: t.coordinateSystem.getRect(),
                    style: o.defaults({
                        fill: t.get("backgroundColor")
                    }, t.getItemStyle()),
                    silent: !0,
                    z2: -1
                }))
            }
        }),
        n.registerPreprocessor(function(t) {
            t.xAxis && t.yAxis && !t.grid && (t.grid = {})
        })
    },
    947: function(t, e, i) {
        function n(t, e) {
            return e.type || (e.data ? "category" : "value")
        }
        var o = i(1)
          , a = i(81)
          , s = i(959)
          , r = i(350)
          , l = a.extend({
            type: "cartesian2dAxis",
            axis: null,
            init: function() {
                l.superApply(this, "init", arguments),
                this.resetRange()
            },
            mergeOption: function() {
                l.superApply(this, "mergeOption", arguments),
                this.resetRange()
            },
            restoreData: function() {
                l.superApply(this, "restoreData", arguments),
                this.resetRange()
            },
            getCoordSysModel: function() {
                return this.ecModel.queryComponents({
                    mainType: "grid",
                    index: this.option.gridIndex,
                    id: this.option.gridId
                })[0]
            }
        });
        o.merge(l.prototype, r);
        var c = {
            offset: 0
        };
        s("x", l, n, c),
        s("y", l, n, c);
        var d = l;
        t.exports = d
    },
    949: function(t, e, i) {
        function n(t, e, i) {
            i = i || {};
            var n = t.coordinateSystem
              , a = e.axis
              , s = {}
              , r = a.getAxesOnZeroOf()[0]
              , l = a.position
              , c = r ? "onZero" : l
              , d = a.dim
              , u = n.getRect()
              , h = [u.x, u.x + u.width, u.y, u.y + u.height]
              , p = {
                left: 0,
                right: 1,
                top: 0,
                bottom: 1,
                onZero: 2
            }
              , g = e.get("offset") || 0
              , f = "x" === d ? [h[2] - g, h[3] + g] : [h[0] - g, h[1] + g];
            if (r) {
                var m = r.toGlobalCoord(r.dataToCoord(0));
                f[p.onZero] = Math.max(Math.min(m, f[1]), f[0])
            }
            s.position = ["y" === d ? f[p[c]] : h[0], "x" === d ? f[p[c]] : h[3]],
            s.rotation = Math.PI / 2 * ("x" === d ? 0 : 1);
            var x = {
                top: -1,
                bottom: 1,
                left: -1,
                right: 1
            };
            s.labelDirection = s.tickDirection = s.nameDirection = x[l],
            s.labelOffset = r ? f[p[l]] - f[p.onZero] : 0,
            e.get("axisTick.inside") && (s.tickDirection = -s.tickDirection),
            o.retrieve(i.labelInside, e.get("axisLabel.inside")) && (s.labelDirection = -s.labelDirection);
            var v = e.get("axisLabel.rotate");
            return s.labelRotate = "top" === c ? -v : v,
            s.z2 = 1,
            s
        }
        var o = i(1);
        e.layout = n
    },
    953: function(t, e, i) {
        function n(t) {
            this.group = new r.Group,
            this._symbolCtor = t || l
        }
        function o(t, e, i, n) {
            return e && !isNaN(e[0]) && !isNaN(e[1]) && !(n.isIgnore && n.isIgnore(i)) && !(n.clipShape && !n.clipShape.contain(e[0], e[1])) && "none" !== t.getItemVisual(i, "symbol")
        }
        function a(t) {
            return null == t || d(t) || (t = {
                isIgnore: t
            }),
            t || {}
        }
        function s(t) {
            var e = t.hostModel;
            return {
                itemStyle: e.getModel("itemStyle").getItemStyle(["color"]),
                hoverItemStyle: e.getModel("emphasis.itemStyle").getItemStyle(),
                symbolRotate: e.get("symbolRotate"),
                symbolOffset: e.get("symbolOffset"),
                hoverAnimation: e.get("hoverAnimation"),
                labelModel: e.getModel("label"),
                hoverLabelModel: e.getModel("emphasis.label"),
                cursorStyle: e.get("cursor")
            }
        }
        var r = i(77)
          , l = i(944)
          , c = i(1)
          , d = c.isObject
          , u = n.prototype;
        u.updateData = function(t, e) {
            e = a(e);
            var i = this.group
              , n = t.hostModel
              , l = this._data
              , c = this._symbolCtor
              , d = s(t);
            l || i.removeAll(),
            t.diff(l).add(function(n) {
                var a = t.getItemLayout(n);
                if (o(t, a, n, e)) {
                    var s = new c(t,n,d);
                    s.attr("position", a),
                    t.setItemGraphicEl(n, s),
                    i.add(s)
                }
            }).update(function(a, s) {
                var u = l.getItemGraphicEl(s)
                  , h = t.getItemLayout(a);
                if (!o(t, h, a, e))
                    return void i.remove(u);
                u ? (u.updateData(t, a, d),
                r.updateProps(u, {
                    position: h
                }, n)) : (u = new c(t,a),
                u.attr("position", h)),
                i.add(u),
                t.setItemGraphicEl(a, u)
            }).remove(function(t) {
                var e = l.getItemGraphicEl(t);
                e && e.fadeOut(function() {
                    i.remove(e)
                })
            }).execute(),
            this._data = t
        }
        ,
        u.isPersistent = function() {
            return !0
        }
        ,
        u.updateLayout = function() {
            var t = this._data;
            t && t.eachItemGraphicEl(function(e, i) {
                var n = t.getItemLayout(i);
                e.attr("position", n)
            })
        }
        ,
        u.incrementalPrepareUpdate = function(t) {
            this._seriesScope = s(t),
            this._data = null,
            this.group.removeAll()
        }
        ,
        u.incrementalUpdate = function(t, e, i) {
            function n(t) {
                t.isGroup || (t.incremental = t.useHoverLayer = !0)
            }
            i = a(i);
            for (var s = t.start; s < t.end; s++) {
                var r = e.getItemLayout(s);
                if (o(e, r, s, i)) {
                    var l = new this._symbolCtor(e,s,this._seriesScope);
                    l.traverse(n),
                    l.attr("position", r),
                    this.group.add(l),
                    e.setItemGraphicEl(s, l)
                }
            }
        }
        ,
        u.remove = function(t) {
            var e = this.group
              , i = this._data;
            i && t ? i.eachItemGraphicEl(function(t) {
                t.fadeOut(function() {
                    e.remove(t)
                })
            }) : e.removeAll()
        }
        ;
        var h = n;
        t.exports = h
    },
    954: function(t, e, i) {
        var n = i(343)
          , o = i(1)
          , a = i(936)
          , s = i(1009);
        i(1007),
        i(1008),
        i(983),
        n.registerPreprocessor(function(t) {
            if (t) {
                (!t.axisPointer || 0 === t.axisPointer.length) && (t.axisPointer = {});
                var e = t.axisPointer.link;
                e && !o.isArray(e) && (t.axisPointer.link = [e])
            }
        }),
        n.registerProcessor(n.PRIORITY.PROCESSOR.STATISTIC, function(t, e) {
            t.getComponent("axisPointer").coordSysAxesInfo = a.collect(t, e)
        }),
        n.registerAction({
            type: "updateAxisPointer",
            event: "updateAxisPointer",
            update: ":updateAxisPointer"
        }, s)
    },
    955: function(t, e, i) {
        function n(t) {
            return {
                seriesType: t,
                plan: s(),
                reset: function(t) {
                    function e(t, e) {
                        for (var i = t.end - t.start, o = s && new Float32Array(i * c), a = t.start, l = 0, d = [], u = []; a < t.end; a++) {
                            var h;
                            if (1 === c) {
                                var p = e.get(r[0], a);
                                h = !isNaN(p) && n.dataToPoint(p, null, u)
                            } else {
                                var p = d[0] = e.get(r[0], a)
                                  , g = d[1] = e.get(r[1], a);
                                h = !isNaN(p) && !isNaN(g) && n.dataToPoint(d, null, u)
                            }
                            s ? (o[l++] = h ? h[0] : NaN,
                            o[l++] = h ? h[1] : NaN) : e.setItemLayout(a, h && h.slice() || [NaN, NaN])
                        }
                        s && e.setLayout("symbolPoints", o)
                    }
                    var i = t.getData()
                      , n = t.coordinateSystem
                      , o = t.pipelineContext
                      , s = o.large;
                    if (n) {
                        var r = a(n.dimensions, function(t) {
                            return i.mapDimension(t)
                        }).slice(0, 2)
                          , c = r.length
                          , d = i.getCalculationInfo("stackResultDimension");
                        return l(i, r[0]) && (r[0] = d),
                        l(i, r[1]) && (r[1] = d),
                        c && {
                            progress: e
                        }
                    }
                }
            }
        }
        var o = i(1)
          , a = o.map
          , s = i(213)
          , r = i(133)
          , l = r.isDimensionStacked;
        t.exports = n
    },
    956: function(t, e, i) {
        function n(t, e, i) {
            var n, a = t.getBaseAxis(), s = t.getOtherAxis(a), l = o(s, i), d = a.dim, u = s.dim, h = e.mapDimension(u), p = e.mapDimension(d), g = "x" === u || "radius" === u ? 1 : 0, f = c(t.dimensions, function(t) {
                return e.mapDimension(t)
            }), m = e.getCalculationInfo("stackResultDimension");
            return (n |= r(e, f[0])) && (f[0] = m),
            (n |= r(e, f[1])) && (f[1] = m),
            {
                dataDimsForPoint: f,
                valueStart: l,
                valueAxisDim: u,
                baseAxisDim: d,
                stacked: !!n,
                valueDim: h,
                baseDim: p,
                baseDataOffset: g,
                stackedOverDimension: e.getCalculationInfo("stackedOverDimension")
            }
        }
        function o(t, e) {
            var i = 0
              , n = t.scale.getExtent();
            return "start" === e ? i = n[0] : "end" === e ? i = n[1] : n[0] > 0 ? i = n[0] : n[1] < 0 && (i = n[1]),
            i
        }
        function a(t, e, i, n) {
            var o = NaN;
            t.stacked && (o = i.get(i.getCalculationInfo("stackedOverDimension"), n)),
            isNaN(o) && (o = t.valueStart);
            var a = t.baseDataOffset
              , s = [];
            return s[a] = i.get(t.baseDim, n),
            s[1 - a] = o,
            e.dataToPoint(s)
        }
        var s = i(133)
          , r = s.isDimensionStacked
          , l = i(1)
          , c = l.map;
        e.prepareDataCoordInfo = n,
        e.getStackedOnPoint = a
    },
    957: function(t, e, i) {
        function n(t, e) {
            var i, n = [], s = t.seriesIndex;
            if (null == s || !(i = e.getSeriesByIndex(s)))
                return {
                    point: []
                };
            var r = i.getData()
              , l = a.queryDataIndex(r, t);
            if (null == l || l < 0 || o.isArray(l))
                return {
                    point: []
                };
            var c = r.getItemGraphicEl(l)
              , d = i.coordinateSystem;
            if (i.getTooltipPosition)
                n = i.getTooltipPosition(l) || [];
            else if (d && d.dataToPoint)
                n = d.dataToPoint(r.getValues(o.map(d.dimensions, function(t) {
                    return r.mapDimension(t)
                }), l, !0)) || [];
            else if (c) {
                var u = c.getBoundingRect().clone();
                u.applyTransform(c.transform),
                n = [u.x + u.width / 2, u.y + u.height / 2]
            }
            return {
                point: n,
                el: c
            }
        }
        var o = i(1)
          , a = i(11);
        t.exports = n
    },
    958: function(t, e, i) {
        function n(t, e, i) {
            if (!u.node) {
                var n = e.getZr();
                g(n).records || (g(n).records = {}),
                o(n, e);
                (g(n).records[t] || (g(n).records[t] = {})).handler = i
            }
        }
        function o(t, e) {
            function i(i, n) {
                t.on(i, function(i) {
                    var o = l(e);
                    f(g(t).records, function(t) {
                        t && n(t, i, o.dispatchAction)
                    }),
                    a(o.pendings, e)
                })
            }
            g(t).initialized || (g(t).initialized = !0,
            i("click", d.curry(r, "click")),
            i("mousemove", d.curry(r, "mousemove")),
            i("globalout", s))
        }
        function a(t, e) {
            var i, n = t.showTip.length, o = t.hideTip.length;
            n ? i = t.showTip[n - 1] : o && (i = t.hideTip[o - 1]),
            i && (i.dispatchAction = null,
            e.dispatchAction(i))
        }
        function s(t, e, i) {
            t.handler("leave", null, i)
        }
        function r(t, e, i, n) {
            e.handler(t, i, n)
        }
        function l(t) {
            var e = {
                showTip: [],
                hideTip: []
            }
              , i = function(n) {
                var o = e[n.type];
                o ? o.push(n) : (n.dispatchAction = i,
                t.dispatchAction(n))
            };
            return {
                dispatchAction: i,
                pendings: e
            }
        }
        function c(t, e) {
            if (!u.node) {
                var i = e.getZr();
                (g(i).records || {})[t] && (g(i).records[t] = null)
            }
        }
        var d = i(1)
          , u = i(31)
          , h = i(11)
          , p = h.makeInner
          , g = p()
          , f = d.each;
        e.register = n,
        e.unregister = c
    },
    959: function(t, e, i) {
        function n(t, e, i, n) {
            o.each(u, function(s) {
                e.extend({
                    type: t + "Axis." + s,
                    mergeDefaultAndTheme: function(e, n) {
                        var a = this.layoutMode
                          , r = a ? l(e) : {}
                          , d = n.getTheme();
                        o.merge(e, d.get(s + "Axis")),
                        o.merge(e, this.getDefaultOption()),
                        e.type = i(t, e),
                        a && c(e, r, a)
                    },
                    optionUpdated: function() {
                        "category" === this.option.type && (this.__ordinalMeta = d.createByAxisModel(this))
                    },
                    getCategories: function(t) {
                        var e = this.option;
                        if ("category" === e.type)
                            return t ? e.data : this.__ordinalMeta.categories
                    },
                    getOrdinalMeta: function() {
                        return this.__ordinalMeta
                    },
                    defaultOption: o.mergeAll([{}, a[s + "Axis"], n], !0)
                })
            }),
            s.registerSubTypeDefaulter(t + "Axis", o.curry(i, t))
        }
        var o = i(1)
          , a = i(978)
          , s = i(81)
          , r = i(132)
          , l = r.getLayoutParams
          , c = r.mergeLayoutParam
          , d = i(354)
          , u = ["value", "category", "time", "log"];
        t.exports = n
    },
    960: function(t, e, i) {
        function n(t, e, i) {
            return t.getCoordSysModel() === e
        }
        function o(t, e, i) {
            this._coordsMap = {},
            this._coordsList = [],
            this._axesMap = {},
            this._axesList = [],
            this._initCartesian(t, e, i),
            this.model = t
        }
        function a(t, e, i, n) {
            function o(t) {
                return t.dim + "_" + t.index
            }
            i.getAxesOnZeroOf = function() {
                return a ? [a] : []
            }
            ;
            var a, r = t[e], l = i.model, c = l.get("axisLine.onZero"), d = l.get("axisLine.onZeroAxisIndex");
            if (c) {
                if (null != d)
                    s(r[d]) && (a = r[d]);
                else
                    for (var u in r)
                        if (r.hasOwnProperty(u) && s(r[u]) && !n[o(r[u])]) {
                            a = r[u];
                            break
                        }
                a && (n[o(a)] = !0)
            }
        }
        function s(t) {
            return t && "category" !== t.type && "time" !== t.type && _(t)
        }
        function r(t, e) {
            var i = t.getExtent()
              , n = i[0] + i[1];
            t.toGlobalCoord = "x" === t.dim ? function(t) {
                return t + e
            }
            : function(t) {
                return n - t + e
            }
            ,
            t.toLocalCoord = "x" === t.dim ? function(t) {
                return t - e
            }
            : function(t) {
                return n - t + e
            }
        }
        function l(t, e) {
            return g(M, function(e) {
                return t.getReferringComponents(e)[0]
            })
        }
        function c(t) {
            return "cartesian2d" === t.get("coordinateSystem")
        }
        var d = i(24)
          , u = (d.__DEV__,
        i(1))
          , h = u.isObject
          , p = u.each
          , g = u.map
          , f = u.indexOf
          , m = (u.retrieve,
        i(132))
          , x = m.getLayoutRect
          , v = i(206)
          , y = v.createScaleByModel
          , _ = v.ifAxisCrossZero
          , b = v.niceScaleExtent
          , w = v.estimateLabelUnionRect
          , S = i(1e3)
          , A = i(998)
          , C = i(210)
          , T = i(133)
          , I = T.getStackedDimension;
        i(1001);
        var D = o.prototype;
        D.type = "grid",
        D.axisPointerEnabled = !0,
        D.getRect = function() {
            return this._rect
        }
        ,
        D.update = function(t, e) {
            var i = this._axesMap;
            this._updateScale(t, this.model),
            p(i.x, function(t) {
                b(t.scale, t.model)
            }),
            p(i.y, function(t) {
                b(t.scale, t.model)
            });
            var n = {};
            p(i.x, function(t) {
                a(i, "y", t, n)
            }),
            p(i.y, function(t) {
                a(i, "x", t, n)
            }),
            this.resize(this.model, e)
        }
        ,
        D.resize = function(t, e, i) {
            function n() {
                p(a, function(t) {
                    var e = t.isHorizontal()
                      , i = e ? [0, o.width] : [0, o.height]
                      , n = t.inverse ? 1 : 0;
                    t.setExtent(i[n], i[1 - n]),
                    r(t, e ? o.x : o.y)
                })
            }
            var o = x(t.getBoxLayoutParams(), {
                width: e.getWidth(),
                height: e.getHeight()
            });
            this._rect = o;
            var a = this._axesList;
            n(),
            !i && t.get("containLabel") && (p(a, function(t) {
                if (!t.model.get("axisLabel.inside")) {
                    var e = w(t);
                    if (e) {
                        var i = t.isHorizontal() ? "height" : "width"
                          , n = t.model.get("axisLabel.margin");
                        o[i] -= e[i] + n,
                        "top" === t.position ? o.y += e.height + n : "left" === t.position && (o.x += e.width + n)
                    }
                }
            }),
            n())
        }
        ,
        D.getAxis = function(t, e) {
            var i = this._axesMap[t];
            if (null != i) {
                if (null == e)
                    for (var n in i)
                        if (i.hasOwnProperty(n))
                            return i[n];
                return i[e]
            }
        }
        ,
        D.getAxes = function() {
            return this._axesList.slice()
        }
        ,
        D.getCartesian = function(t, e) {
            if (null != t && null != e) {
                var i = "x" + t + "y" + e;
                return this._coordsMap[i]
            }
            h(t) && (e = t.yAxisIndex,
            t = t.xAxisIndex);
            for (var n = 0, o = this._coordsList; n < o.length; n++)
                if (o[n].getAxis("x").index === t || o[n].getAxis("y").index === e)
                    return o[n]
        }
        ,
        D.getCartesians = function() {
            return this._coordsList.slice()
        }
        ,
        D.convertToPixel = function(t, e, i) {
            var n = this._findConvertTarget(t, e);
            return n.cartesian ? n.cartesian.dataToPoint(i) : n.axis ? n.axis.toGlobalCoord(n.axis.dataToCoord(i)) : null
        }
        ,
        D.convertFromPixel = function(t, e, i) {
            var n = this._findConvertTarget(t, e);
            return n.cartesian ? n.cartesian.pointToData(i) : n.axis ? n.axis.coordToData(n.axis.toLocalCoord(i)) : null
        }
        ,
        D._findConvertTarget = function(t, e) {
            var i, n, o = e.seriesModel, a = e.xAxisModel || o && o.getReferringComponents("xAxis")[0], s = e.yAxisModel || o && o.getReferringComponents("yAxis")[0], r = e.gridModel, l = this._coordsList;
            if (o)
                i = o.coordinateSystem,
                f(l, i) < 0 && (i = null);
            else if (a && s)
                i = this.getCartesian(a.componentIndex, s.componentIndex);
            else if (a)
                n = this.getAxis("x", a.componentIndex);
            else if (s)
                n = this.getAxis("y", s.componentIndex);
            else if (r) {
                var c = r.coordinateSystem;
                c === this && (i = this._coordsList[0])
            }
            return {
                cartesian: i,
                axis: n
            }
        }
        ,
        D.containPoint = function(t) {
            var e = this._coordsList[0];
            if (e)
                return e.containPoint(t)
        }
        ,
        D._initCartesian = function(t, e, i) {
            function o(i) {
                return function(o, l) {
                    if (n(o, t, e)) {
                        var c = o.get("position");
                        "x" === i ? "top" !== c && "bottom" !== c && (c = "bottom",
                        a[c] && (c = "top" === c ? "bottom" : "top")) : "left" !== c && "right" !== c && (c = "left",
                        a[c] && (c = "left" === c ? "right" : "left")),
                        a[c] = !0;
                        var d = new A(i,y(o),[0, 0],o.get("type"),c)
                          , u = "category" === d.type;
                        d.onBand = u && o.get("boundaryGap"),
                        d.inverse = o.get("inverse"),
                        o.axis = d,
                        d.model = o,
                        d.grid = this,
                        d.index = l,
                        this._axesList.push(d),
                        s[i][l] = d,
                        r[i]++
                    }
                }
            }
            var a = {
                left: !1,
                right: !1,
                top: !1,
                bottom: !1
            }
              , s = {
                x: {},
                y: {}
            }
              , r = {
                x: 0,
                y: 0
            };
            if (e.eachComponent("xAxis", o("x"), this),
            e.eachComponent("yAxis", o("y"), this),
            !r.x || !r.y)
                return this._axesMap = {},
                void (this._axesList = []);
            this._axesMap = s,
            p(s.x, function(e, i) {
                p(s.y, function(n, o) {
                    var a = "x" + i + "y" + o
                      , s = new S(a);
                    s.grid = this,
                    s.model = t,
                    this._coordsMap[a] = s,
                    this._coordsList.push(s),
                    s.addAxis(e),
                    s.addAxis(n)
                }, this)
            }, this)
        }
        ,
        D._updateScale = function(t, e) {
            function i(t, e, i) {
                p(t.mapDimension(e.dim, !0), function(i) {
                    e.scale.unionExtentFromData(t, I(t, i))
                })
            }
            p(this._axesList, function(t) {
                t.scale.setExtent(1 / 0, -1 / 0)
            }),
            t.eachSeries(function(o) {
                if (c(o)) {
                    var a = l(o, t)
                      , s = a[0]
                      , r = a[1];
                    if (!n(s, e, t) || !n(r, e, t))
                        return;
                    var d = this.getCartesian(s.componentIndex, r.componentIndex)
                      , u = o.getData()
                      , h = d.getAxis("x")
                      , p = d.getAxis("y");
                    "list" === u.type && (i(u, h, o),
                    i(u, p, o))
                }
            }, this)
        }
        ,
        D.getTooltipAxes = function(t) {
            var e = []
              , i = [];
            return p(this.getCartesians(), function(n) {
                var o = null != t && "auto" !== t ? n.getAxis(t) : n.getBaseAxis()
                  , a = n.getOtherAxis(o);
                f(e, o) < 0 && e.push(o),
                f(i, a) < 0 && i.push(a)
            }),
            {
                baseAxes: e,
                otherAxes: i
            }
        }
        ;
        var M = ["xAxis", "yAxis"];
        o.create = function(t, e) {
            var i = [];
            return t.eachComponent("grid", function(n, a) {
                var s = new o(n,t,e);
                s.name = "grid_" + a,
                s.resize(n, e, !0),
                n.coordinateSystem = s,
                i.push(s)
            }),
            t.eachSeries(function(e) {
                if (c(e)) {
                    var i = l(e, t)
                      , n = i[0]
                      , o = i[1]
                      , a = n.getCoordSysModel()
                      , s = a.coordinateSystem;
                    e.coordinateSystem = s.getCartesian(n.componentIndex, o.componentIndex)
                }
            }),
            i
        }
        ,
        o.dimensions = o.prototype.dimensions = S.prototype.dimensions,
        C.register("cartesian2d", o);
        var O = o;
        t.exports = O
    },
    961: function(t, e, i) {
        function n(t, e) {
            var i = t.mapDimension("defaultedLabel", !0)
              , n = i.length;
            if (1 === n)
                return a(t, e, i[0]);
            if (n) {
                for (var o = [], s = 0; s < i.length; s++) {
                    var r = a(t, e, i[s]);
                    o.push(r)
                }
                return o.join(" ")
            }
        }
        var o = i(102)
          , a = o.retrieveRawValue;
        e.getDefaultLabel = n
    },
    962: function(t, e, i) {
        var n = i(343);
        i(974),
        i(1010),
        i(975);
        var o = i(1011)
          , a = i(81);
        n.registerProcessor(o),
        a.registerSubTypeDefaulter("legend", function() {
            return "plain"
        })
    },
    971: function(t, e, i) {
        var n = i(343);
        i(1004),
        i(1005);
        var o = i(942)
          , a = i(955)
          , s = i(1016);
        i(946),
        n.registerVisual(o("line", "circle", "line")),
        n.registerLayout(a("line")),
        n.registerProcessor(n.PRIORITY.PROCESSOR.STATISTIC, s("line"))
    },
    972: function(t, e, i) {
        var n = i(343);
        i(954),
        i(1013),
        i(1015),
        n.registerAction({
            type: "showTip",
            event: "showTip",
            update: "tooltip:manuallyShowTip"
        }, function() {}),
        n.registerAction({
            type: "hideTip",
            event: "hideTip",
            update: "tooltip:manuallyHideTip"
        }, function() {})
    },
    973: function(t, e, i) {
        function n() {}
        function o(t, e, i, n) {
            a(x(i).lastProp, n) || (x(i).lastProp = n,
            e ? u.updateProps(i, n, t) : (i.stopAnimation(),
            i.attr(n)))
        }
        function a(t, e) {
            if (c.isObject(t) && c.isObject(e)) {
                var i = !0;
                return c.each(e, function(e, n) {
                    i = i && a(t[n], e)
                }),
                !!i
            }
            return t === e
        }
        function s(t, e) {
            t[e.get("label.show") ? "show" : "hide"]()
        }
        function r(t) {
            return {
                position: t.position.slice(),
                rotation: t.rotation || 0
            }
        }
        function l(t, e, i) {
            var n = e.get("z")
              , o = e.get("zlevel");
            t && t.traverse(function(t) {
                "group" !== t.type && (null != n && (t.z = n),
                null != o && (t.zlevel = o),
                t.silent = i)
            })
        }
        var c = i(1)
          , d = i(53)
          , u = i(77)
          , h = i(936)
          , p = i(100)
          , g = i(211)
          , f = i(11)
          , m = f.makeInner
          , x = m()
          , v = c.clone
          , y = c.bind;
        n.prototype = {
            _group: null,
            _lastGraphicKey: null,
            _handle: null,
            _dragging: !1,
            _lastValue: null,
            _lastStatus: null,
            _payloadInfo: null,
            animationThreshold: 15,
            render: function(t, e, i, n) {
                var a = e.get("value")
                  , s = e.get("status");
                if (this._axisModel = t,
                this._axisPointerModel = e,
                this._api = i,
                n || this._lastValue !== a || this._lastStatus !== s) {
                    this._lastValue = a,
                    this._lastStatus = s;
                    var r = this._group
                      , d = this._handle;
                    if (!s || "hide" === s)
                        return r && r.hide(),
                        void (d && d.hide());
                    r && r.show(),
                    d && d.show();
                    var h = {};
                    this.makeElOption(h, a, t, e, i);
                    var p = h.graphicKey;
                    p !== this._lastGraphicKey && this.clear(i),
                    this._lastGraphicKey = p;
                    var g = this._moveAnimation = this.determineAnimation(t, e);
                    if (r) {
                        var f = c.curry(o, e, g);
                        this.updatePointerEl(r, h, f, e),
                        this.updateLabelEl(r, h, f, e)
                    } else
                        r = this._group = new u.Group,
                        this.createPointerEl(r, h, t, e),
                        this.createLabelEl(r, h, t, e),
                        i.getZr().add(r);
                    l(r, e, !0),
                    this._renderHandle(a)
                }
            },
            remove: function(t) {
                this.clear(t)
            },
            dispose: function(t) {
                this.clear(t)
            },
            determineAnimation: function(t, e) {
                var i = e.get("animation")
                  , n = t.axis
                  , o = "category" === n.type
                  , a = e.get("snap");
                if (!a && !o)
                    return !1;
                if ("auto" === i || null == i) {
                    var s = this.animationThreshold;
                    if (o && n.getBandWidth() > s)
                        return !0;
                    if (a) {
                        var r = h.getAxisInfo(t).seriesDataCount
                          , l = n.getExtent();
                        return Math.abs(l[0] - l[1]) / r > s
                    }
                    return !1
                }
                return !0 === i
            },
            makeElOption: function(t, e, i, n, o) {},
            createPointerEl: function(t, e, i, n) {
                var o = e.pointer;
                if (o) {
                    var a = x(t).pointerEl = new u[o.type](v(e.pointer));
                    t.add(a)
                }
            },
            createLabelEl: function(t, e, i, n) {
                if (e.label) {
                    var o = x(t).labelEl = new u.Rect(v(e.label));
                    t.add(o),
                    s(o, n)
                }
            },
            updatePointerEl: function(t, e, i) {
                var n = x(t).pointerEl;
                n && (n.setStyle(e.pointer.style),
                i(n, {
                    shape: e.pointer.shape
                }))
            },
            updateLabelEl: function(t, e, i, n) {
                var o = x(t).labelEl;
                o && (o.setStyle(e.label.style),
                i(o, {
                    shape: e.label.shape,
                    position: e.label.position
                }),
                s(o, n))
            },
            _renderHandle: function(t) {
                if (!this._dragging && this.updateHandleTransform) {
                    var e = this._axisPointerModel
                      , i = this._api.getZr()
                      , n = this._handle
                      , o = e.getModel("handle")
                      , a = e.get("status");
                    if (!o.get("show") || !a || "hide" === a)
                        return n && i.remove(n),
                        void (this._handle = null);
                    var s;
                    this._handle || (s = !0,
                    n = this._handle = u.createIcon(o.get("icon"), {
                        cursor: "move",
                        draggable: !0,
                        onmousemove: function(t) {
                            p.stop(t.event)
                        },
                        onmousedown: y(this._onHandleDragMove, this, 0, 0),
                        drift: y(this._onHandleDragMove, this),
                        ondragend: y(this._onHandleDragEnd, this)
                    }),
                    i.add(n)),
                    l(n, e, !1);
                    var r = ["color", "borderColor", "borderWidth", "opacity", "shadowColor", "shadowBlur", "shadowOffsetX", "shadowOffsetY"];
                    n.setStyle(o.getItemStyle(null, r));
                    var d = o.get("size");
                    c.isArray(d) || (d = [d, d]),
                    n.attr("scale", [d[0] / 2, d[1] / 2]),
                    g.createOrUpdate(this, "_doDispatchAxisPointer", o.get("throttle") || 0, "fixRate"),
                    this._moveHandleToValue(t, s)
                }
            },
            _moveHandleToValue: function(t, e) {
                o(this._axisPointerModel, !e && this._moveAnimation, this._handle, r(this.getHandleTransform(t, this._axisModel, this._axisPointerModel)))
            },
            _onHandleDragMove: function(t, e) {
                var i = this._handle;
                if (i) {
                    this._dragging = !0;
                    var n = this.updateHandleTransform(r(i), [t, e], this._axisModel, this._axisPointerModel);
                    this._payloadInfo = n,
                    i.stopAnimation(),
                    i.attr(r(n)),
                    x(i).lastProp = null,
                    this._doDispatchAxisPointer()
                }
            },
            _doDispatchAxisPointer: function() {
                if (this._handle) {
                    var t = this._payloadInfo
                      , e = this._axisModel;
                    this._api.dispatchAction({
                        type: "updateAxisPointer",
                        x: t.cursorPoint[0],
                        y: t.cursorPoint[1],
                        tooltipOption: t.tooltipOption,
                        axesInfo: [{
                            axisDim: e.axis.dim,
                            axisIndex: e.componentIndex
                        }]
                    })
                }
            },
            _onHandleDragEnd: function(t) {
                if (this._dragging = !1,
                this._handle) {
                    var e = this._axisPointerModel.get("value");
                    this._moveHandleToValue(e),
                    this._api.dispatchAction({
                        type: "hideTip"
                    })
                }
            },
            getHandleTransform: null,
            updateHandleTransform: null,
            clear: function(t) {
                this._lastValue = null,
                this._lastStatus = null;
                var e = t.getZr()
                  , i = this._group
                  , n = this._handle;
                e && i && (this._lastGraphicKey = null,
                i && e.remove(i),
                n && e.remove(n),
                this._group = null,
                this._handle = null,
                this._payloadInfo = null)
            },
            doClear: function() {},
            buildLabel: function(t, e, i) {
                return i = i || 0,
                {
                    x: t[i],
                    y: t[1 - i],
                    width: e[i],
                    height: e[1 - i]
                }
            }
        },
        n.prototype.constructor = n,
        d.enableClassExtend(n);
        var _ = n;
        t.exports = _
    },
    974: function(t, e, i) {
        var n = i(343)
          , o = i(1)
          , a = i(82)
          , s = i(11)
          , r = s.isNameSpecified
          , l = n.extendComponentModel({
            type: "legend.plain",
            dependencies: ["series"],
            layoutMode: {
                type: "box",
                ignoreSize: !0
            },
            init: function(t, e, i) {
                this.mergeDefaultAndTheme(t, i),
                t.selected = t.selected || {}
            },
            mergeOption: function(t) {
                l.superCall(this, "mergeOption", t)
            },
            optionUpdated: function() {
                this._updateData(this.ecModel);
                var t = this._data;
                if (t[0] && "single" === this.get("selectedMode")) {
                    for (var e = !1, i = 0; i < t.length; i++) {
                        var n = t[i].get("name");
                        if (this.isSelected(n)) {
                            this.select(n),
                            e = !0;
                            break
                        }
                    }
                    !e && this.select(t[0].get("name"))
                }
            },
            _updateData: function(t) {
                var e = []
                  , i = [];
                t.eachRawSeries(function(n) {
                    var o = n.name;
                    i.push(o);
                    var a;
                    if (n.legendDataProvider) {
                        var s = n.legendDataProvider()
                          , l = s.mapArray(s.getName);
                        t.isSeriesFiltered(n) || (i = i.concat(l)),
                        l.length ? e = e.concat(l) : a = !0
                    } else
                        a = !0;
                    a && r(n) && e.push(n.name)
                }),
                this._availableNames = i;
                var n = this.get("data") || e
                  , s = o.map(n, function(t) {
                    return "string" != typeof t && "number" != typeof t || (t = {
                        name: t
                    }),
                    new a(t,this,this.ecModel)
                }, this);
                this._data = s
            },
            getData: function() {
                return this._data
            },
            select: function(t) {
                var e = this.option.selected;
                if ("single" === this.get("selectedMode")) {
                    var i = this._data;
                    o.each(i, function(t) {
                        e[t.get("name")] = !1
                    })
                }
                e[t] = !0
            },
            unSelect: function(t) {
                "single" !== this.get("selectedMode") && (this.option.selected[t] = !1)
            },
            toggleSelected: function(t) {
                var e = this.option.selected;
                e.hasOwnProperty(t) || (e[t] = !0),
                this[e[t] ? "unSelect" : "select"](t)
            },
            isSelected: function(t) {
                var e = this.option.selected;
                return !(e.hasOwnProperty(t) && !e[t]) && o.indexOf(this._availableNames, t) >= 0
            },
            defaultOption: {
                zlevel: 0,
                z: 4,
                show: !0,
                orient: "horizontal",
                left: "center",
                top: 0,
                align: "auto",
                backgroundColor: "rgba(0,0,0,0)",
                borderColor: "#ccc",
                borderRadius: 0,
                borderWidth: 0,
                padding: 5,
                itemGap: 10,
                itemWidth: 25,
                itemHeight: 14,
                inactiveColor: "#ccc",
                textStyle: {
                    color: "#333"
                },
                selectedMode: !0,
                tooltip: {
                    show: !1
                }
            }
        })
          , c = l;
        t.exports = c
    },
    975: function(t, e, i) {
        function n(t, e) {
            e.dispatchAction({
                type: "legendToggleSelect",
                name: t
            })
        }
        function o(t, e, i, n) {
            var o = i.getZr().storage.getDisplayList()[0];
            o && o.useHoverLayer || i.dispatchAction({
                type: "highlight",
                seriesName: t,
                name: e,
                excludeSeriesId: n
            })
        }
        function a(t, e, i, n) {
            var o = i.getZr().storage.getDisplayList()[0];
            o && o.useHoverLayer || i.dispatchAction({
                type: "downplay",
                seriesName: t,
                name: e,
                excludeSeriesId: n
            })
        }
        var s = i(24)
          , r = (s.__DEV__,
        i(343))
          , l = i(1)
          , c = i(345)
          , d = c.createSymbol
          , u = i(77)
          , h = i(985)
          , p = h.makeBackground
          , g = i(132)
          , f = l.curry
          , m = l.each
          , x = u.Group
          , v = r.extendComponentView({
            type: "legend.plain",
            newlineDisabled: !1,
            init: function() {
                this.group.add(this._contentGroup = new x),
                this._backgroundEl,
                this._isFirstRender = !0
            },
            getContentGroup: function() {
                return this._contentGroup
            },
            render: function(t, e, i) {
                var n = this._isFirstRender;
                if (this._isFirstRender = !1,
                this.resetInner(),
                t.get("show", !0)) {
                    var o = t.get("align");
                    o && "auto" !== o || (o = "right" === t.get("left") && "vertical" === t.get("orient") ? "right" : "left"),
                    this.renderInner(o, t, e, i);
                    var a = t.getBoxLayoutParams()
                      , s = {
                        width: i.getWidth(),
                        height: i.getHeight()
                    }
                      , r = t.get("padding")
                      , c = g.getLayoutRect(a, s, r)
                      , d = this.layoutInner(t, o, c, n)
                      , u = g.getLayoutRect(l.defaults({
                        width: d.width,
                        height: d.height
                    }, a), s, r);
                    this.group.attr("position", [u.x - d.x, u.y - d.y]),
                    this.group.add(this._backgroundEl = p(d, t))
                }
            },
            resetInner: function() {
                this.getContentGroup().removeAll(),
                this._backgroundEl && this.group.remove(this._backgroundEl)
            },
            renderInner: function(t, e, i, s) {
                var r = this.getContentGroup()
                  , c = l.createHashMap()
                  , d = e.get("selectedMode")
                  , u = [];
                i.eachRawSeries(function(t) {
                    !t.get("legendHoverLink") && u.push(t.id)
                }),
                m(e.getData(), function(l, h) {
                    var p = l.get("name");
                    if (!this.newlineDisabled && ("" === p || "\n" === p))
                        return void r.add(new x({
                            newline: !0
                        }));
                    var g = i.getSeriesByName(p)[0];
                    if (!c.get(p))
                        if (g) {
                            var m = g.getData()
                              , v = m.getVisual("color");
                            "function" == typeof v && (v = v(g.getDataParams(0)));
                            var y = m.getVisual("legendSymbol") || "roundRect"
                              , _ = m.getVisual("symbol")
                              , b = this._createItem(p, h, l, e, y, _, t, v, d);
                            b.on("click", f(n, p, s)).on("mouseover", f(o, g.name, null, s, u)).on("mouseout", f(a, g.name, null, s, u)),
                            c.set(p, !0)
                        } else
                            i.eachRawSeries(function(i) {
                                if (!c.get(p) && i.legendDataProvider) {
                                    var r = i.legendDataProvider()
                                      , g = r.indexOfName(p);
                                    if (g < 0)
                                        return;
                                    var m = r.getItemVisual(g, "color");
                                    this._createItem(p, h, l, e, "roundRect", null, t, m, d).on("click", f(n, p, s)).on("mouseover", f(o, null, p, s, u)).on("mouseout", f(a, null, p, s, u)),
                                    c.set(p, !0)
                                }
                            }, this)
                }, this)
            },
            _createItem: function(t, e, i, n, o, a, s, r, c) {
                var h = n.get("itemWidth")
                  , p = n.get("itemHeight")
                  , g = n.get("inactiveColor")
                  , f = n.get("symbolKeepAspect")
                  , m = n.isSelected(t)
                  , v = new x
                  , y = i.getModel("textStyle")
                  , _ = i.get("icon")
                  , b = i.getModel("tooltip")
                  , w = b.parentModel;
                if (o = _ || o,
                v.add(d(o, 0, 0, h, p, m ? r : g, null == f || f)),
                !_ && a && (a !== o || "none" === a)) {
                    var S = .8 * p;
                    "none" === a && (a = "circle"),
                    v.add(d(a, (h - S) / 2, (p - S) / 2, S, S, m ? r : g, null == f || f))
                }
                var A = "left" === s ? h + 5 : -5
                  , C = s
                  , T = n.get("formatter")
                  , I = t;
                "string" == typeof T && T ? I = T.replace("{name}", null != t ? t : "") : "function" == typeof T && (I = T(t)),
                v.add(new u.Text({
                    style: u.setTextStyle({}, y, {
                        text: I,
                        x: A,
                        y: p / 2,
                        textFill: m ? y.getTextColor() : g,
                        textAlign: C,
                        textVerticalAlign: "middle"
                    })
                }));
                var D = new u.Rect({
                    shape: v.getBoundingRect(),
                    invisible: !0,
                    tooltip: b.get("show") ? l.extend({
                        content: t,
                        formatter: w.get("formatter", !0) || function() {
                            return t
                        }
                        ,
                        formatterParams: {
                            componentType: "legend",
                            legendIndex: n.componentIndex,
                            name: t,
                            $vars: ["name"]
                        }
                    }, b.option) : null
                });
                return v.add(D),
                v.eachChild(function(t) {
                    t.silent = !0
                }),
                D.silent = !c,
                this.getContentGroup().add(v),
                u.setHoverStyle(v),
                v.__legendDataIndex = e,
                v
            },
            layoutInner: function(t, e, i) {
                var n = this.getContentGroup();
                g.box(t.get("orient"), n, t.get("itemGap"), i.width, i.height);
                var o = n.getBoundingRect();
                return n.attr("position", [-o.x, -o.y]),
                this.group.getBoundingRect()
            },
            remove: function() {
                this.getContentGroup().removeAll(),
                this._isFirstRender = !0
            }
        });
        t.exports = v
    },
    976: function(t, e, i) {
        var n = i(343)
          , o = i(77)
          , a = i(132)
          , s = a.getLayoutRect;
        n.extendComponentModel({
            type: "title",
            layoutMode: {
                type: "box",
                ignoreSize: !0
            },
            defaultOption: {
                zlevel: 0,
                z: 6,
                show: !0,
                text: "",
                target: "blank",
                subtext: "",
                subtarget: "blank",
                left: 0,
                top: 0,
                backgroundColor: "rgba(0,0,0,0)",
                borderColor: "#ccc",
                borderWidth: 0,
                padding: 5,
                itemGap: 10,
                textStyle: {
                    fontSize: 18,
                    fontWeight: "bolder",
                    color: "#333"
                },
                subtextStyle: {
                    color: "#aaa"
                }
            }
        }),
        n.extendComponentView({
            type: "title",
            render: function(t, e, i) {
                if (this.group.removeAll(),
                t.get("show")) {
                    var n = this.group
                      , a = t.getModel("textStyle")
                      , r = t.getModel("subtextStyle")
                      , l = t.get("textAlign")
                      , c = t.get("textBaseline")
                      , d = new o.Text({
                        style: o.setTextStyle({}, a, {
                            text: t.get("text"),
                            textFill: a.getTextColor()
                        }, {
                            disableBox: !0
                        }),
                        z2: 10
                    })
                      , u = d.getBoundingRect()
                      , h = t.get("subtext")
                      , p = new o.Text({
                        style: o.setTextStyle({}, r, {
                            text: h,
                            textFill: r.getTextColor(),
                            y: u.height + t.get("itemGap"),
                            textVerticalAlign: "top"
                        }, {
                            disableBox: !0
                        }),
                        z2: 10
                    })
                      , g = t.get("link")
                      , f = t.get("sublink")
                      , m = t.get("triggerEvent", !0);
                    d.silent = !g && !m,
                    p.silent = !f && !m,
                    g && d.on("click", function() {
                        window.open(g, "_" + t.get("target"))
                    }),
                    f && p.on("click", function() {
                        window.open(f, "_" + t.get("subtarget"))
                    }),
                    d.eventData = p.eventData = m ? {
                        componentType: "title",
                        componentIndex: t.componentIndex
                    } : null,
                    n.add(d),
                    h && n.add(p);
                    var x = n.getBoundingRect()
                      , v = t.getBoxLayoutParams();
                    v.width = x.width,
                    v.height = x.height;
                    var y = s(v, {
                        width: i.getWidth(),
                        height: i.getHeight()
                    }, t.get("padding"));
                    l || (l = t.get("left") || t.get("right"),
                    "middle" === l && (l = "center"),
                    "right" === l ? y.x += y.width : "center" === l && (y.x += y.width / 2)),
                    c || (c = t.get("top") || t.get("bottom"),
                    "center" === c && (c = "middle"),
                    "bottom" === c ? y.y += y.height : "middle" === c && (y.y += y.height / 2),
                    c = c || "top"),
                    n.attr("position", [y.x, y.y]);
                    var _ = {
                        textAlign: l,
                        textVerticalAlign: c
                    };
                    d.setStyle(_),
                    p.setStyle(_),
                    x = n.getBoundingRect();
                    var b = y.margin
                      , w = t.getItemStyle(["color", "opacity"]);
                    w.fill = t.get("backgroundColor");
                    var S = new o.Rect({
                        shape: {
                            x: x.x - b[3],
                            y: x.y - b[0],
                            width: x.width + b[1] + b[3],
                            height: x.height + b[0] + b[2],
                            r: t.get("borderRadius")
                        },
                        style: w,
                        silent: !0
                    });
                    o.subPixelOptimizeRect(S),
                    n.add(S)
                }
            }
        })
    },
    978: function(t, e, i) {
        var n = i(1)
          , o = {
            show: !0,
            zlevel: 0,
            z: 0,
            inverse: !1,
            name: "",
            nameLocation: "end",
            nameRotate: null,
            nameTruncate: {
                maxWidth: null,
                ellipsis: "...",
                placeholder: "."
            },
            nameTextStyle: {},
            nameGap: 15,
            silent: !1,
            triggerEvent: !1,
            tooltip: {
                show: !1
            },
            axisPointer: {},
            axisLine: {
                show: !0,
                onZero: !0,
                onZeroAxisIndex: null,
                lineStyle: {
                    color: "#333",
                    width: 1,
                    type: "solid"
                },
                symbol: ["none", "none"],
                symbolSize: [10, 15]
            },
            axisTick: {
                show: !0,
                inside: !1,
                length: 5,
                lineStyle: {
                    width: 1
                }
            },
            axisLabel: {
                show: !0,
                inside: !1,
                rotate: 0,
                showMinLabel: null,
                showMaxLabel: null,
                margin: 8,
                fontSize: 12
            },
            splitLine: {
                show: !0,
                lineStyle: {
                    color: ["#ccc"],
                    width: 1,
                    type: "solid"
                }
            },
            splitArea: {
                show: !1,
                areaStyle: {
                    color: ["rgba(250,250,250,0.3)", "rgba(200,200,200,0.3)"]
                }
            }
        }
          , a = {};
        a.categoryAxis = n.merge({
            boundaryGap: !0,
            deduplication: null,
            splitLine: {
                show: !1
            },
            axisTick: {
                alignWithLabel: !1,
                interval: "auto"
            },
            axisLabel: {
                interval: "auto"
            }
        }, o),
        a.valueAxis = n.merge({
            boundaryGap: [0, 0],
            splitNumber: 5
        }, o),
        a.timeAxis = n.defaults({
            scale: !0,
            min: "dataMin",
            max: "dataMax"
        }, a.valueAxis),
        a.logAxis = n.defaults({
            scale: !0,
            logBase: 10
        }, a.valueAxis);
        var s = a;
        t.exports = s
    },
    982: function(t, e, i) {
        function n(t) {
            return isNaN(t[0]) || isNaN(t[1])
        }
        function o(t, e, i, n, o, r, l, c, d, u, h) {
            return "none" !== u && u ? a.apply(this, arguments) : s.apply(this, arguments)
        }
        function a(t, e, i, o, a, s, r, l, c, d, u) {
            for (var h = 0, p = i, f = 0; f < o; f++) {
                var v = e[p];
                if (p >= a || p < 0)
                    break;
                if (n(v)) {
                    if (u) {
                        p += s;
                        continue
                    }
                    break
                }
                if (p === i)
                    t[s > 0 ? "moveTo" : "lineTo"](v[0], v[1]);
                else if (c > 0) {
                    var y = e[h]
                      , _ = "y" === d ? 1 : 0
                      , b = (v[_] - y[_]) * c;
                    g(m, y),
                    m[_] = y[_] + b,
                    g(x, v),
                    x[_] = v[_] - b,
                    t.bezierCurveTo(m[0], m[1], x[0], x[1], v[0], v[1])
                } else
                    t.lineTo(v[0], v[1]);
                h = p,
                p += s
            }
            return f
        }
        function s(t, e, i, o, a, s, r, l, d, v, y) {
            for (var _ = 0, b = i, w = 0; w < o; w++) {
                var S = e[b];
                if (b >= a || b < 0)
                    break;
                if (n(S)) {
                    if (y) {
                        b += s;
                        continue
                    }
                    break
                }
                if (b === i)
                    t[s > 0 ? "moveTo" : "lineTo"](S[0], S[1]),
                    g(m, S);
                else if (d > 0) {
                    var A = b + s
                      , C = e[A];
                    if (y)
                        for (; C && n(e[A]); )
                            A += s,
                            C = e[A];
                    var T = .5
                      , I = e[_]
                      , C = e[A];
                    if (!C || n(C))
                        g(x, S);
                    else {
                        n(C) && !y && (C = S),
                        c.sub(f, C, I);
                        var D, M;
                        if ("x" === v || "y" === v) {
                            var O = "x" === v ? 0 : 1;
                            D = Math.abs(S[O] - I[O]),
                            M = Math.abs(S[O] - C[O])
                        } else
                            D = c.dist(S, I),
                            M = c.dist(S, C);
                        T = M / (M + D),
                        p(x, S, f, -d * (1 - T))
                    }
                    u(m, m, l),
                    h(m, m, r),
                    u(x, x, l),
                    h(x, x, r),
                    t.bezierCurveTo(m[0], m[1], x[0], x[1], S[0], S[1]),
                    p(m, S, f, d * T)
                } else
                    t.lineTo(S[0], S[1]);
                _ = b,
                b += s
            }
            return w
        }
        function r(t, e) {
            var i = [1 / 0, 1 / 0]
              , n = [-1 / 0, -1 / 0];
            if (e)
                for (var o = 0; o < t.length; o++) {
                    var a = t[o];
                    a[0] < i[0] && (i[0] = a[0]),
                    a[1] < i[1] && (i[1] = a[1]),
                    a[0] > n[0] && (n[0] = a[0]),
                    a[1] > n[1] && (n[1] = a[1])
                }
            return {
                min: e ? i : n,
                max: e ? n : i
            }
        }
        var l = i(15)
          , c = i(17)
          , d = i(357)
          , u = c.min
          , h = c.max
          , p = c.scaleAndAdd
          , g = c.copy
          , f = []
          , m = []
          , x = []
          , v = l.extend({
            type: "ec-polyline",
            shape: {
                points: [],
                smooth: 0,
                smoothConstraint: !0,
                smoothMonotone: null,
                connectNulls: !1
            },
            style: {
                fill: null,
                stroke: "#000"
            },
            brush: d(l.prototype.brush),
            buildPath: function(t, e) {
                var i = e.points
                  , a = 0
                  , s = i.length
                  , l = r(i, e.smoothConstraint);
                if (e.connectNulls) {
                    for (; s > 0 && n(i[s - 1]); s--)
                        ;
                    for (; a < s && n(i[a]); a++)
                        ;
                }
                for (; a < s; )
                    a += o(t, i, a, s, s, 1, l.min, l.max, e.smooth, e.smoothMonotone, e.connectNulls) + 1
            }
        })
          , y = l.extend({
            type: "ec-polygon",
            shape: {
                points: [],
                stackedOnPoints: [],
                smooth: 0,
                stackedOnSmooth: 0,
                smoothConstraint: !0,
                smoothMonotone: null,
                connectNulls: !1
            },
            brush: d(l.prototype.brush),
            buildPath: function(t, e) {
                var i = e.points
                  , a = e.stackedOnPoints
                  , s = 0
                  , l = i.length
                  , c = e.smoothMonotone
                  , d = r(i, e.smoothConstraint)
                  , u = r(a, e.smoothConstraint);
                if (e.connectNulls) {
                    for (; l > 0 && n(i[l - 1]); l--)
                        ;
                    for (; s < l && n(i[s]); s++)
                        ;
                }
                for (; s < l; ) {
                    var h = o(t, i, s, l, l, 1, d.min, d.max, e.smooth, c, e.connectNulls);
                    o(t, a, s + h - 1, h, l, -1, u.min, u.max, e.stackedOnSmooth, c, e.connectNulls),
                    s += h + 1,
                    t.closePath()
                }
            }
        });
        e.Polyline = v,
        e.Polygon = y
    },
    983: function(t, e, i) {
        function n(t, e) {
            var i = {};
            return i[e.dim + "AxisIndex"] = e.index,
            t.getCartesian(i)
        }
        function o(t) {
            return "x" === t.dim ? 0 : 1
        }
        var a = i(77)
          , s = i(973)
          , r = i(945)
          , l = i(949)
          , c = i(939)
          , d = s.extend({
            makeElOption: function(t, e, i, o, a) {
                var s = i.axis
                  , c = s.grid
                  , d = o.get("type")
                  , h = n(c, s).getOtherAxis(s).getGlobalExtent()
                  , p = s.toGlobalCoord(s.dataToCoord(e, !0));
                if (d && "none" !== d) {
                    var g = r.buildElStyle(o)
                      , f = u[d](s, p, h, g);
                    f.style = g,
                    t.graphicKey = f.type,
                    t.pointer = f
                }
                var m = l.layout(c.model, i);
                r.buildCartesianSingleLabelElOption(e, t, m, i, o, a)
            },
            getHandleTransform: function(t, e, i) {
                var n = l.layout(e.axis.grid.model, e, {
                    labelInside: !1
                });
                return n.labelMargin = i.get("handle.margin"),
                {
                    position: r.getTransformedPosition(e.axis, t, n),
                    rotation: n.rotation + (n.labelDirection < 0 ? Math.PI : 0)
                }
            },
            updateHandleTransform: function(t, e, i, o) {
                var a = i.axis
                  , s = a.grid
                  , r = a.getGlobalExtent(!0)
                  , l = n(s, a).getOtherAxis(a).getGlobalExtent()
                  , c = "x" === a.dim ? 0 : 1
                  , d = t.position;
                d[c] += e[c],
                d[c] = Math.min(r[1], d[c]),
                d[c] = Math.max(r[0], d[c]);
                var u = (l[1] + l[0]) / 2
                  , h = [u, u];
                h[c] = d[c];
                var p = [{
                    verticalAlign: "middle"
                }, {
                    align: "center"
                }];
                return {
                    position: d,
                    rotation: t.rotation,
                    cursorPoint: h,
                    tooltipOption: p[c]
                }
            }
        })
          , u = {
            line: function(t, e, i, n) {
                var s = r.makeLineShape([e, i[0]], [e, i[1]], o(t));
                return a.subPixelOptimizeLine({
                    shape: s,
                    style: n
                }),
                {
                    type: "Line",
                    shape: s
                }
            },
            shadow: function(t, e, i, n) {
                var a = Math.max(1, t.getBandWidth())
                  , s = i[1] - i[0];
                return {
                    type: "Rect",
                    shape: r.makeRectShape([e - a / 2, i[0]], [a, s], o(t))
                }
            }
        };
        c.registerAxisPointerClass("CartesianAxisPointer", d);
        var h = d;
        t.exports = h
    },
    984: function(t, e, i) {
        function n(t, e, i, n) {
            var o = i.type
              , a = f[o.charAt(0).toUpperCase() + o.slice(1)]
              , s = new a(i);
            e.add(s),
            n.set(t, s),
            s.__ecGraphicId = t
        }
        function o(t, e) {
            var i = t && t.parent;
            i && ("group" === t.type && t.traverse(function(t) {
                o(t, e)
            }),
            e.removeKey(t.__ecGraphicId),
            i.remove(t))
        }
        function a(t) {
            return t = p.extend({}, t),
            p.each(["id", "parentId", "$action", "hv", "bounding"].concat(m.LOCATION_PARAMS), function(e) {
                delete t[e]
            }),
            t
        }
        function s(t, e) {
            var i;
            return p.each(e, function(e) {
                null != t[e] && "auto" !== t[e] && (i = !0)
            }),
            i
        }
        function r(t, e) {
            var i = t.exist;
            if (e.id = t.keyInfo.id,
            !e.type && i && (e.type = i.type),
            null == e.parentId) {
                var n = e.parentOption;
                n ? e.parentId = n.id : i && (e.parentId = i.parentId)
            }
            e.parentOption = null
        }
        function l(t, e, i) {
            var n = p.extend({}, i)
              , o = t[e]
              , a = i.$action || "merge";
            "merge" === a ? o ? (p.merge(o, n, !0),
            m.mergeLayoutParam(o, n, {
                ignoreSize: !0
            }),
            m.copyLayoutParams(i, o)) : t[e] = n : "replace" === a ? t[e] = n : "remove" === a && o && (t[e] = null)
        }
        function c(t, e) {
            t && (t.hv = e.hv = [s(e, ["left", "right"]), s(e, ["top", "bottom"])],
            "group" === t.type && (null == t.width && (t.width = e.width = 0),
            null == t.height && (t.height = e.height = 0)))
        }
        function d(t, e, i) {
            var n = t.eventData;
            t.silent || t.ignore || n || (n = t.eventData = {
                componentType: "graphic",
                componentIndex: e.componentIndex,
                name: t.name
            }),
            n && (n.info = t.info)
        }
        var u = i(24)
          , h = (u.__DEV__,
        i(343))
          , p = i(1)
          , g = i(11)
          , f = i(77)
          , m = i(132);
        h.registerPreprocessor(function(t) {
            var e = t.graphic;
            p.isArray(e) ? e[0] && e[0].elements ? t.graphic = [t.graphic[0]] : t.graphic = [{
                elements: e
            }] : e && !e.elements && (t.graphic = [{
                elements: [e]
            }])
        });
        var x = h.extendComponentModel({
            type: "graphic",
            defaultOption: {
                elements: [],
                parentId: null
            },
            _elOptionsToUpdate: null,
            mergeOption: function(t) {
                var e = this.option.elements;
                this.option.elements = null,
                x.superApply(this, "mergeOption", arguments),
                this.option.elements = e
            },
            optionUpdated: function(t, e) {
                var i = this.option
                  , n = (e ? i : t).elements
                  , o = i.elements = e ? [] : i.elements
                  , a = [];
                this._flatten(n, a);
                var s = g.mappingToExists(o, a);
                g.makeIdAndName(s);
                var d = this._elOptionsToUpdate = [];
                p.each(s, function(t, e) {
                    var i = t.option;
                    i && (d.push(i),
                    r(t, i),
                    l(o, e, i),
                    c(o[e], i))
                }, this);
                for (var u = o.length - 1; u >= 0; u--)
                    null == o[u] ? o.splice(u, 1) : delete o[u].$action
            },
            _flatten: function(t, e, i) {
                p.each(t, function(t) {
                    if (t) {
                        i && (t.parentOption = i),
                        e.push(t);
                        var n = t.children;
                        "group" === t.type && n && this._flatten(n, e, t),
                        delete t.children
                    }
                }, this)
            },
            useElOptionsToUpdate: function() {
                var t = this._elOptionsToUpdate;
                return this._elOptionsToUpdate = null,
                t
            }
        });
        h.extendComponentView({
            type: "graphic",
            init: function(t, e) {
                this._elMap = p.createHashMap(),
                this._lastGraphicModel
            },
            render: function(t, e, i) {
                t !== this._lastGraphicModel && this._clear(),
                this._lastGraphicModel = t,
                this._updateElements(t),
                this._relocate(t, i)
            },
            _updateElements: function(t) {
                var e = t.useElOptionsToUpdate();
                if (e) {
                    var i = this._elMap
                      , s = this.group;
                    p.each(e, function(e) {
                        var r = e.$action
                          , l = e.id
                          , c = i.get(l)
                          , u = e.parentId
                          , h = null != u ? i.get(u) : s
                          , p = e.style;
                        "text" === e.type && p && (e.hv && e.hv[1] && (p.textVerticalAlign = p.textBaseline = null),
                        !p.hasOwnProperty("textFill") && p.fill && (p.textFill = p.fill),
                        !p.hasOwnProperty("textStroke") && p.stroke && (p.textStroke = p.stroke));
                        var g = a(e);
                        r && "merge" !== r ? "replace" === r ? (o(c, i),
                        n(l, h, g, i)) : "remove" === r && o(c, i) : c ? c.attr(g) : n(l, h, g, i);
                        var f = i.get(l);
                        f && (f.__ecGraphicWidth = e.width,
                        f.__ecGraphicHeight = e.height,
                        d(f, t, e))
                    })
                }
            },
            _relocate: function(t, e) {
                for (var i = t.option.elements, n = this.group, o = this._elMap, a = i.length - 1; a >= 0; a--) {
                    var s = i[a]
                      , r = o.get(s.id);
                    if (r) {
                        var l = r.parent
                          , c = l === n ? {
                            width: e.getWidth(),
                            height: e.getHeight()
                        } : {
                            width: l.__ecGraphicWidth || 0,
                            height: l.__ecGraphicHeight || 0
                        };
                        m.positionElement(r, s, c, null, {
                            hv: s.hv,
                            boundingMode: s.bounding
                        })
                    }
                }
            },
            _clear: function() {
                var t = this._elMap;
                t.each(function(e) {
                    o(e, t)
                }),
                this._elMap = p.createHashMap()
            },
            dispose: function() {
                this._clear()
            }
        })
    },
    985: function(t, e, i) {
        function n(t, e, i) {
            var n = e.getBoxLayoutParams()
              , o = e.get("padding")
              , a = {
                width: i.getWidth(),
                height: i.getHeight()
            }
              , c = s(n, a, o);
            r(e.get("orient"), t, e.get("itemGap"), c.width, c.height),
            l(t, n, a, o)
        }
        function o(t, e) {
            var i = c.normalizeCssArray(e.get("padding"))
              , n = e.getItemStyle(["color", "opacity"]);
            n.fill = e.get("backgroundColor");
            var t = new d.Rect({
                shape: {
                    x: t.x - i[3],
                    y: t.y - i[0],
                    width: t.width + i[1] + i[3],
                    height: t.height + i[0] + i[2],
                    r: e.get("borderRadius")
                },
                style: n,
                silent: !0,
                z2: -1
            });
            return t
        }
        var a = i(132)
          , s = a.getLayoutRect
          , r = a.box
          , l = a.positionElement
          , c = i(68)
          , d = i(77);
        e.layout = n,
        e.makeBackground = o
    },
    995: function(t, e, i) {
        i(947),
        i(996)
    },
    996: function(t, e, i) {
        var n = i(1)
          , o = i(77)
          , a = i(938)
          , s = i(939)
          , r = i(949)
          , l = ["axisLine", "axisTickLabel", "axisName"]
          , c = ["splitArea", "splitLine"]
          , d = s.extend({
            type: "cartesianAxis",
            axisPointerClass: "CartesianAxisPointer",
            render: function(t, e, i, s) {
                this.group.removeAll();
                var u = this._axisGroup;
                if (this._axisGroup = new o.Group,
                this.group.add(this._axisGroup),
                t.get("show")) {
                    var h = t.getCoordSysModel()
                      , p = r.layout(h, t)
                      , g = new a(t,p);
                    n.each(l, g.add, g),
                    this._axisGroup.add(g.getGroup()),
                    n.each(c, function(e) {
                        t.get(e + ".show") && this["_" + e](t, h)
                    }, this),
                    o.groupTransition(u, this._axisGroup, t),
                    d.superCall(this, "render", t, e, i, s)
                }
            },
            remove: function() {
                this._splitAreaColors = null
            },
            _splitLine: function(t, e) {
                var i = t.axis;
                if (!i.scale.isBlank()) {
                    var a = t.getModel("splitLine")
                      , s = a.getModel("lineStyle")
                      , r = s.get("color");
                    r = n.isArray(r) ? r : [r];
                    for (var l = e.coordinateSystem.getRect(), c = i.isHorizontal(), d = 0, u = i.getTicksCoords({
                        tickModel: a
                    }), h = [], p = [], g = s.getLineStyle(), f = 0; f < u.length; f++) {
                        var m = i.toGlobalCoord(u[f].coord);
                        c ? (h[0] = m,
                        h[1] = l.y,
                        p[0] = m,
                        p[1] = l.y + l.height) : (h[0] = l.x,
                        h[1] = m,
                        p[0] = l.x + l.width,
                        p[1] = m);
                        var x = d++ % r.length
                          , v = u[f].tickValue;
                        this._axisGroup.add(new o.Line(o.subPixelOptimizeLine({
                            anid: null != v ? "line_" + u[f].tickValue : null,
                            shape: {
                                x1: h[0],
                                y1: h[1],
                                x2: p[0],
                                y2: p[1]
                            },
                            style: n.defaults({
                                stroke: r[x]
                            }, g),
                            silent: !0
                        })))
                    }
                }
            },
            _splitArea: function(t, e) {
                var i = t.axis;
                if (!i.scale.isBlank()) {
                    var a = t.getModel("splitArea")
                      , s = a.getModel("areaStyle")
                      , r = s.get("color")
                      , l = e.coordinateSystem.getRect()
                      , c = i.getTicksCoords({
                        tickModel: a,
                        clamp: !0
                    });
                    if (c.length) {
                        var d = r.length
                          , u = this._splitAreaColors
                          , h = n.createHashMap()
                          , p = 0;
                        if (u)
                            for (var g = 0; g < c.length; g++) {
                                var f = u.get(c[g].tickValue);
                                if (null != f) {
                                    p = (f + (d - 1) * g) % d;
                                    break
                                }
                            }
                        var m = i.toGlobalCoord(c[0].coord)
                          , x = s.getAreaStyle();
                        r = n.isArray(r) ? r : [r];
                        for (var g = 1; g < c.length; g++) {
                            var v, y, _, b, w = i.toGlobalCoord(c[g].coord);
                            i.isHorizontal() ? (v = m,
                            y = l.y,
                            _ = w - v,
                            b = l.height,
                            m = v + _) : (v = l.x,
                            y = m,
                            _ = l.width,
                            b = w - y,
                            m = y + b);
                            var S = c[g - 1].tickValue;
                            null != S && h.set(S, p),
                            this._axisGroup.add(new o.Rect({
                                anid: null != S ? "area_" + S : null,
                                shape: {
                                    x: v,
                                    y: y,
                                    width: _,
                                    height: b
                                },
                                style: n.defaults({
                                    fill: r[p]
                                }, x),
                                silent: !0
                            })),
                            p = (p + 1) % d
                        }
                        this._splitAreaColors = h
                    }
                }
            }
        });
        d.extend({
            type: "xAxis"
        }),
        d.extend({
            type: "yAxis"
        })
    },
    998: function(t, e, i) {
        var n = i(1)
          , o = i(348)
          , a = function(t, e, i, n, a) {
            o.call(this, t, e, i),
            this.type = n || "value",
            this.position = a || "bottom"
        };
        a.prototype = {
            constructor: a,
            index: 0,
            getAxesOnZeroOf: null,
            model: null,
            isHorizontal: function() {
                var t = this.position;
                return "top" === t || "bottom" === t
            },
            getGlobalExtent: function(t) {
                var e = this.getExtent();
                return e[0] = this.toGlobalCoord(e[0]),
                e[1] = this.toGlobalCoord(e[1]),
                t && e[0] > e[1] && e.reverse(),
                e
            },
            getOtherAxis: function() {
                this.grid.getOtherAxis()
            },
            pointToData: function(t, e) {
                return this.coordToData(this.toLocalCoord(t["x" === this.dim ? 0 : 1]), e)
            },
            toLocalCoord: null,
            toGlobalCoord: null
        },
        n.inherits(a, o);
        var s = a;
        t.exports = s
    },
    999: function(t, e, i) {
        function n(t) {
            return this._axes[t]
        }
        var o = i(1)
          , a = function(t) {
            this._axes = {},
            this._dimList = [],
            this.name = t || ""
        };
        a.prototype = {
            constructor: a,
            type: "cartesian",
            getAxis: function(t) {
                return this._axes[t]
            },
            getAxes: function() {
                return o.map(this._dimList, n, this)
            },
            getAxesByScale: function(t) {
                return t = t.toLowerCase(),
                o.filter(this.getAxes(), function(e) {
                    return e.scale.type === t
                })
            },
            addAxis: function(t) {
                var e = t.dim;
                this._axes[e] = t,
                this._dimList.push(e)
            },
            dataToCoord: function(t) {
                return this._dataCoordConvert(t, "dataToCoord")
            },
            coordToData: function(t) {
                return this._dataCoordConvert(t, "coordToData")
            },
            _dataCoordConvert: function(t, e) {
                for (var i = this._dimList, n = t instanceof Array ? [] : {}, o = 0; o < i.length; o++) {
                    var a = i[o]
                      , s = this._axes[a];
                    n[a] = s[e](t[a])
                }
                return n
            }
        };
        var s = a;
        t.exports = s
    }
});
