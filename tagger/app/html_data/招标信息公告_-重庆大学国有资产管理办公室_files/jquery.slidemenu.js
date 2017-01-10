if (!mlddm_shiftx) {
    var mlddm_shiftx = 0;
    var mlddm_shifty = 0;
    var mlddm_timeout = 500;
    var mlddm_effect = 'none';
    var mlddm_effect_speed = 300;
    var mlddm_orientation = 'h';
    var mlddm_md = 0;
}
var MLDDM_CLASS = 'mlddm';
var obj_menu = new Array();
function mlddminit(md7) {
    mlddm_md = md7;
    var candidates = document.getElementsByTagName('ul');
    var index = 0;
    for (var i = 0; i < candidates.length; i++) {
        if (candidates[i].className == MLDDM_CLASS) {
            candidates[i].style.visibility = 'visible';
            var obj = candidates[i];
            var value = obj.getAttribute('params');
            obj_menu[index] = new menu(obj, index, value);
            index++;
        }
    }
}
function layer(handler) {
    this.handler = handler;
    this.showed = false;
    this.level = 0;
    this.outerwidth = 0;
    this.outerheight = 0;
    this.innerwidth = 0;
    this.innerheight = 0;
    this.x = 0;
    this.y = 0;
    this.border = 0;
    this.topmargin = 0;
    this.shifter = 0;
    this.parentindex = 0;
    this.reverse = false;
    this.timeouts = new Array();
    this.degree = 0;
}
function menu(obj, obj_n, params) {
    var _2 = obj;
    var _7 = obj_n;
    var _1 = this;
    var _6 = null;
    var _9 = true;
    var _13 = null;
    var _8 = mlddm_shiftx;
    var _11 = mlddm_shifty;
    var _14 = mlddm_timeout;
    var _4 = mlddm_effect;
    var _3 = mlddm_effect_speed;
    var _5 = mlddm_orientation;
    var params_array;
    if (params) {
        params_array = params.split(",");
        if (params_array[0]) _8 = params_array[0] * 1;
        if (params_array[1]) _11 = params_array[1] * 1;
        if (params_array[2]) _14 = params_array[2] * 1;
        if (params_array[3]) _4 = params_array[3];
        if (params_array[4]) _3 = params_array[4] * 1;
        if (params_array[5]) _5 = params_array[5];
        if (!_3) _3 = 1000;
    }
    this._0 = new Array();
    function opacity(index, opac_start, opac_end, speed) {
        var current_layer = _1._0[index];
        for (var z = 0; z < current_layer.timeouts.length; z++) clearTimeout(current_layer.timeouts[z]);
        var degree = current_layer.degree;
        var speed = Math.round(1000 / speed);
        var timer = 0;
        if (degree < opac_end) {
            for (var i = degree; i <= opac_end; i = i + 4) {
                current_layer.timeouts[timer] = setTimeout("changeOpac(" + _7 + "," + index + "," + i + ")", (timer * speed));
                timer++;
            }
        } else if (degree > opac_end) {
            for (var i = degree; i >= opac_end; i = i - 4) {
                current_layer.timeouts[timer] = setTimeout("changeOpac(" + _7 + "," + index + "," + i + ")", (timer * speed));
                timer++;
            }
        }
    }
    function slide(index, direction, speed) {
        var current_layer = _1._0[index];
        for (var z = 0; z < current_layer.timeouts.length; z++) clearTimeout(current_layer.timeouts[z]);
        var degree = current_layer.degree;
        var speed = Math.round(1000 / speed);
        var timer = 0;
        if (_5 == 'h') _10 = 0;
        else _10 = 1;
        if (direction == 'show') {
            for (i = degree; i <= 100; i = i + 2) {
                current_layer.timeouts[timer] = setTimeout("changePOS(" + _7 + "," + index + "," + i + "," + _10 + ")", (timer * speed));
                timer++
            }
        } else if (direction == 'hide') {
            for (i = degree; i >= 0; i = i - 2) {
                current_layer.timeouts[timer] = setTimeout("changePOS(" + _7 + "," + index + "," + i + "," + _10 + ")", (timer * speed));
                timer++;
            }
        }
    }
    function mopen(index) {
        if (!_1._0[index].showed && (mlddm_md == 375)) {
            if (_4 == 'fade') opacity(index, 0, 100, _3);
            else if (_4 == 'slide') slide(index, 'show', _3);
            else _1._0[index].handler.style.visibility = 'visible';
            button_on(_1._0[index].handler);
            _1._0[index].showed = true;
        }
    }
    function mclose(index) {
        if (_1._0[index].showed) {
            if (_4 == 'fade') opacity(index, 100, 0, _3);
            else if (_4 == 'slide') slide(index, 'hide', _3);
            else _1._0[index].handler.style.visibility = 'hidden';
            button_off(_1._0[index].handler);
            _1._0[index].showed = false;
        }
    }
    function getlevel(layer) {
        var level = 0;
        var currentobj = layer;
        while (currentobj.className != MLDDM_CLASS) {
            if (currentobj.nodeName == 'UL') level++;
            currentobj = currentobj.parentNode;
        }
        return level;
    }
    function getbutton(layer) {
        var button;
        var currobj = layer;
        var index = 0;
        while (currobj.className != MLDDM_CLASS) {
            if (currobj.nodeName == 'LI') {
                index++;
                button = currobj;
            }
            currobj = currobj.parentNode;
        }
        return button;
    }
    function button_on(layer) {
        if (getlevel(layer) != 1) return -1;
        var button = getbutton(layer);
        if (button) {
            button = button.getElementsByTagName("a")[0];
            button.id = 'buttonhover';
        }
    }
    function button_off(layer) {
        if (getlevel(layer) != 1) return -1;
        var button = getbutton(layer);
        if (button) {
            button = button.getElementsByTagName("a")[0];
            button.id = 'buttonnohover';
        }
    }
    function getlayerindex(obj) {
        for (i = 0; i < _1._0.length; i++) {
            if (_1._0[i].handler == obj) return i;
        }
        return -1;
    }
    function getparentindex(layer) {
        while (layer.className != MLDDM_CLASS) {
            layer = layer.parentNode;
            if (layer.nodeName == 'UL') return getlayerindex(layer);
        }
        return -1;
    }
    function gettopmargin(obj) {
        var top = obj.offsetTop;
        obj.style.marginTop = '0px';
        var margintop = top - obj.offsetTop;
        obj.style.marginTop = margintop + 'px';
        return margintop;
    }
    function getparentheight(layer) {
        while (layer.className != MLDDM_CLASS) {
            layer = layer.parentNode;
            if (layer.nodeName == 'LI') break;
        }
        return layer.getElementsByTagName("a")[0].offsetHeight;
    }
    function closeall() {
        for (var i = 0; i < _1._0.length; i++) {
            mclose(i);
        }
    }
    function mclosetime() {
        _6 = window.setTimeout(closeall, _14);
    }
    function mcancelclosetime() {
        if (_6) {
            window.clearTimeout(_6);
            _6 = null;
        }
    }
    function setpositions(client_width, scroll_left) {
        var max_right = client_width + scroll_left;
        for (var i = 0; i < _1._0.length; i++) {
            if (_1._0[i].level > 1) {
                _1._0[i].handler.style.left = _1._0[i].x + 'px';
                _1._0[i].reverse = false;
            }
        }
        for (var i = 0; i < _1._0.length; i++) {
            var current_layer = _1._0[i];
            if (current_layer.level > 1) {
                var layer_width = current_layer.outerwidth;
                var border_width = current_layer.border;
                var layer_absx = findPos(current_layer.handler)[0];
                if ((layer_absx + layer_width + border_width * current_layer.level - border_width) > max_right) {
                    current_layer.handler.style.left = -layer_width - _8 + 'px';
                    current_layer.reverse = true;
                }
            }
        }
    }
    this.pcloseall = function () {
        closeall();
    };
    this.eventresize = function () {
        setpositions(getClientWidth(), getScrollLeft());
    };
    this.eventscroll = function () {
        setpositions(getClientWidth(), getScrollLeft());
    };
    this.eventover = function () {
        if (_9) {
            _9 = false;
            mcancelclosetime();
            var currentli = this;
            var layer = currentli.getElementsByTagName("ul")[0];
            var ind = getlayerindex(layer);
            if (ind >= 0) mopen(ind);
            var open_layers = new Array();
            open_layers[0] = currentli.getElementsByTagName("ul")[0];
            if (!open_layers[0]) open_layers[0] = 0;
            var currobj = currentli.parentNode;
            var num = 0;
            while (currobj.className != MLDDM_CLASS) {
                if (currobj.nodeName == 'UL') {
                    num++;
                    open_layers[num] = currobj;
                }
                currobj = currobj.parentNode;
            }
            var layers_to_hide = new Array(_1._0.length);
            for (var i = 0; i < layers_to_hide.length; i++) layers_to_hide[i] = false;
            for (var i = 0; i < open_layers.length; i++) layers_to_hide[getlayerindex(open_layers[i])] = true;
            for (var i = 0; i < layers_to_hide.length; i++) if (!layers_to_hide[i] && (_13 != open_layers[0])) mclose(i);
            _13 = open_layers[1];
        }
    };
    this.eventout = function () {
        _9 = true;
    };
    this.allout = function () {
        mclosetime();
    };
    this.allover = function () {
        mcancelclosetime();
    };
    var _12 = 0;
    if (document.getElementById('debug')) _12 = document.getElementById('debug');
    _12.value = '';
    var css = _2.style.cssText;
    _2.style.cssText = 'visibility:visible;float:left;border-width:0px;margin:0;padding:0';
    _2.style.cssText = ';width:' + _2.offsetWidth + 'px;' + 'height:' + _2.offsetHeight + 'px;' + css;
    var all_li = _2.getElementsByTagName("li");
    this._0[0] = new layer(_2);
    for (var z = 0; z < all_li.length; z++) {
        var layer_handler = all_li[z].getElementsByTagName("ul")[0];
        if (layer_handler) this._0[this._0.length] = new layer(layer_handler);
        all_li[z].onmouseover = this.eventover;
        all_li[z].onmouseout = this.eventout
    }
    _2.onmouseout = this.allout;
    _2.onmouseover = this.allover;
    window.onresize = this.eventresize;
    window.onscroll = this.eventscroll;
    for (var num = 1; num < this._0.length; num++) {
        var nodes = this._0[num].handler.childNodes;
        var specific_nodes = new Array();
        var maxwidth = 0;
        for (i = 0; i < nodes.length; i++) {
            if (!is_ignorable(nodes[i]) && nodes[i].childNodes[0] && nodes[i].childNodes[0].nodeName != 'A') {
                nodes[i].style.display = 'none';
                specific_nodes[specific_nodes.length] = nodes[i];
            }
        }
        for (j = 0; j < nodes.length; j++) {
            if (!is_ignorable(nodes[j]) && nodes[j].childNodes[0] && nodes[j].childNodes[0].nodeName == 'A') {
                var width = nodes[j].childNodes[0].offsetWidth;
                if (width > maxwidth) maxwidth = width;
            }
        }
        for (z = 0; z < specific_nodes.length; z++) specific_nodes[z].style.display = 'inline';
        this._0[num].handler.style.width = maxwidth + 'px';
    }
    for (var num = 0; num < this._0.length; num++) {
        var current_layer = this._0[num];
        current_layer.level = getlevel(current_layer.handler);
        current_layer.parentindex = getparentindex(current_layer.handler);
        current_layer.outerwidth = current_layer.handler.offsetWidth;
        current_layer.outerheight = current_layer.handler.offsetHeight;
        current_layer.innerwidth = current_layer.handler.getElementsByTagName("li")[0].childNodes[0].offsetWidth;
        current_layer.innerheight = 0;
        current_layer.border = (current_layer.outerwidth - current_layer.innerwidth) / 2;
        current_layer.topmargin = gettopmargin(current_layer.handler);
        current_layer.shifter = getparentheight(current_layer.handler)
    }
    for (var num = 0; num < this._0.length; num++) {
        var level = this._0[num].level;
        var current_layer = this._0[num];
        if ((_5 == 'h' && level > 1) || (_5 == 'v' && level > 0)) {
            current_layer.x = this._0[current_layer.parentindex].innerwidth + _8;
            current_layer.y = current_layer.handler.offsetTop - current_layer.topmargin - current_layer.shifter + _11;
            current_layer.handler.style.left = current_layer.x + 'px';
            current_layer.handler.style.top = current_layer.y + 'px';
        }
    }
    setpositions(getClientWidth(), getScrollLeft())
}
function changeOpac(obj_num, layer_num, opacity) {
    var object = obj_menu[obj_num];
    var layer = object._0[layer_num];
    layer.degree = opacity;
    layer.handler.style.opacity = (opacity / 100);
    layer.handler.style.MozOpacity = (opacity / 100);
    layer.handler.style.KhtmlOpacity = (opacity / 100);
    layer.handler.style.filter = "alpha(opacity=" + opacity + ")";
    if (opacity > 98) layer.handler.style.filter = 'none';
    if (opacity > 0) layer.handler.style.visibility = 'visible';
    if (opacity <= 0) layer.handler.style.visibility = 'hidden';
}
function changePOS(obj_num, layer_num, pos, ori) {
    var object = obj_menu[obj_num];
    var layer = object._0[layer_num];
    var level = layer.level;
    var width = layer.outerwidth;
    var height = layer.outerheight;
    var margintop = layer.topmargin;
    var reverse = layer.reverse;
    layer.degree = pos;
    if (!reverse) {
        if (level == 1 && ori == 0) {
            var h = height - pos * height / 100;
            layer.handler.style.clip = 'rect(' + h + 'px 2000px 2000px 0px)';
            layer.handler.style.marginTop = -h + margintop + 'px';
        } else {
            var w = width - pos * width / 100;
            layer.handler.style.clip = 'rect(0px 2000px 2000px ' + w + 'px)';
            layer.handler.style.marginLeft = -w + 'px';
        }
    } else {
        var w = width - pos * width / 100;
        var mw = width - w;
        layer.handler.style.clip = 'rect(0px ' + mw + 'px 2000px 0px)';
        layer.handler.style.marginLeft = w + 'px';
    }
    if (pos <= 0) {
        layer.handler.style.visibility = 'hidden';
        layer.handler.style.clip = 'rect(-2000px, 2000px, 2000px, -2000px)';
        layer.handler.style.marginLeft = 'auto';
    }
    if (pos > 0) {
        layer.handler.style.visibility = 'visible';
    }
    if (pos > 98) {
        layer.handler.style.clip = 'rect(-2000px, 2000px, 2000px, -2000px)';
        layer.handler.style.marginLeft = 'auto';
    }
}
function close() {
    for (var i = 0; i < obj_menu.length; i++) {
        obj_menu[i].pcloseall();
    }
}
document.onclick = close;
function is_all_ws(nod) {
    return !(/[^\t\n\r ]/.test(nod.data));
}
function is_ignorable(nod) {
    return (nod.nodeType == 8) || ((nod.nodeType == 3) && is_all_ws(nod));
}
function node_after(sib) {
    while ((sib = sib.nextSibling)) {
        if (!is_ignorable(sib)) return sib;
    }
    return null;
}
function getClientWidth() {
    return document.documentElement.clientWidth;
}
function getClientHeight() {
    return document.documentElement.clientHeight;
}
function getScrollLeft() {
    return document.compatMode == 'CSS1Compat' && !window.opera ? document.documentElement.scrollLeft : document.body.scrollLeft;
}
function findPos(obj) {
    var curleft = curtop = 0;
    if (obj.offsetParent) {
        do {
            curleft += obj.offsetLeft;
            curtop += obj.offsetTop;
        }
        while (obj = obj.offsetParent)
    }
    return [curleft, curtop];
}