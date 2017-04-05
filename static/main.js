!function(a,b){"function"==typeof define&&define.amd?define([],b):"undefined"!=typeof module&&module.exports?module.exports=b():a.ReconnectingWebSocket=b()}(this,function(){function a(b,c,d){function l(a,b){var c=document.createEvent("CustomEvent");return c.initCustomEvent(a,!1,!1,b),c}var e={debug:!1,automaticOpen:!0,reconnectInterval:1e3,maxReconnectInterval:3e4,reconnectDecay:1.5,timeoutInterval:2e3};d||(d={});for(var f in e)this[f]="undefined"!=typeof d[f]?d[f]:e[f];this.url=b,this.reconnectAttempts=0,this.readyState=WebSocket.CONNECTING,this.protocol=null;var h,g=this,i=!1,j=!1,k=document.createElement("div");k.addEventListener("open",function(a){g.onopen(a)}),k.addEventListener("close",function(a){g.onclose(a)}),k.addEventListener("connecting",function(a){g.onconnecting(a)}),k.addEventListener("message",function(a){g.onmessage(a)}),k.addEventListener("error",function(a){g.onerror(a)}),this.addEventListener=k.addEventListener.bind(k),this.removeEventListener=k.removeEventListener.bind(k),this.dispatchEvent=k.dispatchEvent.bind(k),this.open=function(b){h=new WebSocket(g.url,c||[]),b||k.dispatchEvent(l("connecting")),(g.debug||a.debugAll)&&console.debug("ReconnectingWebSocket","attempt-connect",g.url);var d=h,e=setTimeout(function(){(g.debug||a.debugAll)&&console.debug("ReconnectingWebSocket","connection-timeout",g.url),j=!0,d.close(),j=!1},g.timeoutInterval);h.onopen=function(){clearTimeout(e),(g.debug||a.debugAll)&&console.debug("ReconnectingWebSocket","onopen",g.url),g.protocol=h.protocol,g.readyState=WebSocket.OPEN,g.reconnectAttempts=0;var d=l("open");d.isReconnect=b,b=!1,k.dispatchEvent(d)},h.onclose=function(c){if(clearTimeout(e),h=null,i)g.readyState=WebSocket.CLOSED,k.dispatchEvent(l("close"));else{g.readyState=WebSocket.CONNECTING;var d=l("connecting");d.code=c.code,d.reason=c.reason,d.wasClean=c.wasClean,k.dispatchEvent(d),b||j||((g.debug||a.debugAll)&&console.debug("ReconnectingWebSocket","onclose",g.url),k.dispatchEvent(l("close")));var e=g.reconnectInterval*Math.pow(g.reconnectDecay,g.reconnectAttempts);setTimeout(function(){g.reconnectAttempts++,g.open(!0)},e>g.maxReconnectInterval?g.maxReconnectInterval:e)}},h.onmessage=function(b){(g.debug||a.debugAll)&&console.debug("ReconnectingWebSocket","onmessage",g.url,b.data);var c=l("message");c.data=b.data,k.dispatchEvent(c)},h.onerror=function(b){(g.debug||a.debugAll)&&console.debug("ReconnectingWebSocket","onerror",g.url,b),k.dispatchEvent(l("error"))}},1==this.automaticOpen&&this.open(!1),this.send=function(b){if(h)return(g.debug||a.debugAll)&&console.debug("ReconnectingWebSocket","send",g.url,b),h.send(b);throw"INVALID_STATE_ERR : Pausing to reconnect websocket"},this.close=function(a,b){"undefined"==typeof a&&(a=1e3),i=!0,h&&h.close(a,b)},this.refresh=function(){h&&h.close()}}return a.prototype.onopen=function(){},a.prototype.onclose=function(){},a.prototype.onconnecting=function(){},a.prototype.onmessage=function(){},a.prototype.onerror=function(){},a.debugAll=!1,a.CONNECTING=WebSocket.CONNECTING,a.OPEN=WebSocket.OPEN,a.CLOSING=WebSocket.CLOSING,a.CLOSED=WebSocket.CLOSED,a});

$(function(){

    function highlightLines(){

        $('td').removeClass('hll');

        var hash = window.location.hash.substr(1);

        $.each(hash.split(','), function(index, range){
            var parts = range.split('-');
            var start = parseInt(parts[0].replace(/\D/g,''));
            var end = parseInt(parts[parts.length - 1].replace(/\D/g,''));

            for (i = start; i <= end; i++){
                $('#L' + i).next().addClass('hll');
            }

        });
    }

    highlightLines();
    window.addEventListener("hashchange", highlightLines, false);

    var higlighted = [];
    var lastLineClicked = undefined;

    $('.lineno').click(function(ev){
        var lineno = ev.target.dataset.lineNumber;
        var hash;

        var lines = [lastLineClicked, lineno].filter(Boolean).sort();

        if (lines.length == 2 && ev.shiftKey){
            hash = '#L' + lines[0]+ '-L' + lines[1];
        } else if (lines.length == 2 && (ev.altKey || ev.ctrlKey)){
            hash = '#L' + lines[0]+ ',L' + lines[1];
        } else {
            highlighted = [];
            hash = '#L' + lineno;
        }
        location.href = hash;
        lastLineClicked = lineno;
    });

    $('.line').click(function(ev){

        var tr = $(ev.target.closest('tr'));
        var next = $(tr).next();
        if (next.hasClass("comment")){
            next.remove();
            return;
        }


        var line = ev.target.closest('td').previousSibling.dataset.lineNumber;
        var comment_row = $('#template tr').clone();
        $(comment_row).find('#line').val(line);
        tr.after(comment_row);
    });

    var notifications = false;

    if ("Notification" in window){
        if (Notification.permission === "granted") {
            notifications = true;
        } else if (Notification.permission !== "defined"){
            Notification.requestPermission(function (permission) {
                if (permission === "granted") notifications = true;
            });
        }
    }


    var paste_id = window.location.pathname.slice(1);
    var protocol = window.location.protocol == "https:" ? "wss" : "ws";
    var ws = protocol + '://' + document.domain + ':' + location.port + '/_notify';

    var seen = [];
    var isActive;

    $(window).on("focus", function () {
      isActive = true;
    });

    $(window).on("blur", function () {
      isActive = false;
    });

    if (paste_id && !paste_id.startsWith("_")){
        var notifySocket = new ReconnectingWebSocket(ws);
        notifySocket.onmessage = function (event) {
            var data = JSON.parse(event.data);
            if (data.paste_id != paste_id) return;

            if (seen.indexOf(data.comment_id) > -1) return;
            seen.push(data.comment_id);

            var col_row = $("#C" + data.lineno);
            if(col_row.length){
                col_row.replaceWith($(data.html));
            } else {
                $("#L" + data.lineno).closest('tr').after($(data.html));
            }

            if (!isActive) new Notification("New comment on paste " + paste_id);
        }
    }

});
