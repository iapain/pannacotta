/*
 * jquery.tools 1.1.2 - The missing UI library for the Web
 * 
 * [tools.overlay-1.1.2, tools.expose-1.0.5]
 * 
 * Copyright (c) 2009 Tero Piirainen
 * http://flowplayer.org/tools/
 *
 * Dual licensed under MIT and GPL 2+ licenses
 * http://www.opensource.org/licenses
 * 
 * -----
 * 
 * File generated: Thu Apr 08 06:21:08 GMT 2010
 */
(function(c){c.tools=c.tools||{};c.tools.overlay={version:"1.1.2",addEffect:function(e,f,g){b[e]=[f,g]},conf:{top:"10%",left:"center",absolute:false,speed:"normal",closeSpeed:"fast",effect:"default",close:null,oneInstance:true,closeOnClick:true,closeOnEsc:true,api:false,expose:null,target:null}};var b={};c.tools.overlay.addEffect("default",function(e){this.getOverlay().fadeIn(this.getConf().speed,e)},function(e){this.getOverlay().fadeOut(this.getConf().closeSpeed,e)});var d=[];function a(g,k){var o=this,m=c(this),n=c(window),j,i,h,e=k.expose&&c.tools.expose.version;var f=k.target||g.attr("rel");i=f?c(f):null||g;if(!i.length){throw"Could not find Overlay: "+f}if(g&&g.index(i)==-1){g.click(function(p){o.load(p);return p.preventDefault()})}c.each(k,function(p,q){if(c.isFunction(q)){m.bind(p,q)}});c.extend(o,{load:function(u){if(o.isOpened()){return o}var r=b[k.effect];if(!r){throw'Overlay: cannot find effect : "'+k.effect+'"'}if(k.oneInstance){c.each(d,function(){this.close(u)})}u=u||c.Event();u.type="onBeforeLoad";m.trigger(u);if(u.isDefaultPrevented()){return o}h=true;if(e){i.expose().load(u)}var t=k.top;var s=k.left;var p=i.outerWidth({margin:true});var q=i.outerHeight({margin:true});if(typeof t=="string"){t=t=="center"?Math.max((n.height()-q)/2,0):parseInt(t,10)/100*n.height()}if(s=="center"){s=Math.max((n.width()-p)/2,0)}if(!k.absolute){t+=n.scrollTop();s+=n.scrollLeft()}i.css({top:t,left:s,position:"absolute"});u.type="onStart";m.trigger(u);r[0].call(o,function(){if(h){u.type="onLoad";m.trigger(u)}});if(k.closeOnClick){c(document).bind("click.overlay",function(w){if(!o.isOpened()){return}var v=c(w.target);if(v.parents(i).length>1){return}c.each(d,function(){this.close(w)})})}if(k.closeOnEsc){c(document).unbind("keydown.overlay").bind("keydown.overlay",function(v){if(v.keyCode==27){c.each(d,function(){this.close(v)})}})}return o},close:function(q){if(!o.isOpened()){return o}q=q||c.Event();q.type="onBeforeClose";m.trigger(q);if(q.isDefaultPrevented()){return}h=false;b[k.effect][1].call(o,function(){q.type="onClose";m.trigger(q)});var p=true;c.each(d,function(){if(this.isOpened()){p=false}});if(p){c(document).unbind("click.overlay").unbind("keydown.overlay")}return o},getContent:function(){return i},getOverlay:function(){return i},getTrigger:function(){return g},getClosers:function(){return j},isOpened:function(){return h},getConf:function(){return k},bind:function(p,q){m.bind(p,q);return o},unbind:function(p){m.unbind(p);return o}});c.each("onBeforeLoad,onStart,onLoad,onBeforeClose,onClose".split(","),function(p,q){o[q]=function(r){return o.bind(q,r)}});if(e){if(typeof k.expose=="string"){k.expose={color:k.expose}}c.extend(k.expose,{api:true,closeOnClick:k.closeOnClick,closeOnEsc:false});var l=i.expose(k.expose);l.onBeforeClose(function(p){o.close(p)});o.onClose(function(p){l.close(p)})}j=i.find(k.close||".close");if(!j.length&&!k.close){j=c('<div class="close"></div>');i.prepend(j)}j.click(function(p){o.close(p)})}c.fn.overlay=function(e){var f=this.eq(typeof e=="number"?e:0).data("overlay");if(f){return f}if(c.isFunction(e)){e={onBeforeLoad:e}}var g=c.extend({},c.tools.overlay.conf);e=c.extend(true,g,e);this.each(function(){f=new a(c(this),e);d.push(f);c(this).data("overlay",f)});return e.api?f:this}})(jQuery);
(function(b){b.tools=b.tools||{};b.tools.expose={version:"1.0.5",conf:{maskId:null,loadSpeed:"slow",closeSpeed:"fast",closeOnClick:true,closeOnEsc:true,zIndex:9998,opacity:0.8,color:"#456",api:false}};function a(){if(b.browser.msie){var f=b(document).height(),e=b(window).height();return[window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth,f-e<20?e:f]}return[b(window).width(),b(document).height()]}function c(h,g){var e=this,j=b(this),d=null,f=false,i=0;b.each(g,function(k,l){if(b.isFunction(l)){j.bind(k,l)}});b(window).resize(function(){e.fit()});b.extend(this,{getMask:function(){return d},getExposed:function(){return h},getConf:function(){return g},isLoaded:function(){return f},load:function(n){if(f){return e}i=h.eq(0).css("zIndex");if(g.maskId){d=b("#"+g.maskId)}if(!d||!d.length){var l=a();d=b("<div/>").css({position:"absolute",top:0,left:0,width:l[0],height:l[1],display:"none",opacity:0,zIndex:g.zIndex});if(g.maskId){d.attr("id",g.maskId)}b("body").append(d);var k=d.css("backgroundColor");if(!k||k=="transparent"||k=="rgba(0, 0, 0, 0)"){d.css("backgroundColor",g.color)}if(g.closeOnEsc){b(document).bind("keydown.unexpose",function(o){if(o.keyCode==27){e.close()}})}if(g.closeOnClick){d.bind("click.unexpose",function(o){e.close(o)})}}n=n||b.Event();n.type="onBeforeLoad";j.trigger(n);if(n.isDefaultPrevented()){return e}b.each(h,function(){var o=b(this);if(!/relative|absolute|fixed/i.test(o.css("position"))){o.css("position","relative")}});h.css({zIndex:Math.max(g.zIndex+1,i=="auto"?0:i)});var m=d.height();if(!this.isLoaded()){d.css({opacity:0,display:"block"}).fadeTo(g.loadSpeed,g.opacity,function(){if(d.height()!=m){d.css("height",m)}n.type="onLoad";j.trigger(n)})}f=true;return e},close:function(k){if(!f){return e}k=k||b.Event();k.type="onBeforeClose";j.trigger(k);if(k.isDefaultPrevented()){return e}d.fadeOut(g.closeSpeed,function(){k.type="onClose";j.trigger(k);h.css({zIndex:b.browser.msie?i:null})});f=false;return e},fit:function(){if(d){var k=a();d.css({width:k[0],height:k[1]})}},bind:function(k,l){j.bind(k,l);return e},unbind:function(k){j.unbind(k);return e}});b.each("onBeforeLoad,onLoad,onBeforeClose,onClose".split(","),function(k,l){e[l]=function(m){return e.bind(l,m)}})}b.fn.expose=function(d){var e=this.eq(typeof d=="number"?d:0).data("expose");if(e){return e}if(typeof d=="string"){d={color:d}}var f=b.extend({},b.tools.expose.conf);d=b.extend(f,d);this.each(function(){e=new c(b(this),d);b(this).data("expose",e)});return d.api?e:this}})(jQuery);

