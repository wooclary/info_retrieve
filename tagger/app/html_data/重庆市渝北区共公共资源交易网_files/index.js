/**
 *	渝北公共资源交互
 *	author: zhangzj;
 **/

 (function($) {
    $('#slider').Xslider({
        affect: 'scrollx', //fade 淡入淡出；scrollx 水平轮播； scrolly 垂直轮播
        speed: 1200,
        space: 4000,
        conbox: '.conbox',
        ctag: '.ctag',
        switcher: '.switcher',
        stag: '.stag',
        current: 'cur',
        trigger: 'click'
    });
})(jQuery);


// tab
(function(win, $) {
    // TAB切换,依赖于tabview.js组件
    $(".tab-view").each(function(index, el) {
        new TabView({
            dom: el,
            triggerEvent: 'mouseover',
            activeCls: 'cur'
        });
    });

}(this, jQuery));

//IE placeholder不支持
(function($) {
    $('input, textarea').placeholder();
})(jQuery);
