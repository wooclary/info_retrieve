/*!
 * 轮播图组件js
 * author: zhuyichao
 * 2015.4
 * v 1.1.2
 * 只适用于图片和切换按钮在一个dom容器内的；
 */

/*
 * 轮播图组件
 */
$.fn.Xslider = function(options) {
    var settings = {
        // 效果  有scrollx|scrolly|fade
        affect: 'fade',
        // 动画速度
        speed: 1200,
        // 时间间隔
        space: 2000,
        // 自动滚动
        auto: true,
        // 触发事件 注意用mouseover代替hover
        trigger: 'mouseover',
        // 内容容器id或class
        conbox: '.conbox',
        // 内容标签 默认为<a>
        ctag: '.ctag',
        // 切换触发器id或class
        switcher: '.switcher',
        // 切换器标签 默认为a 
        stag: '.stag',
        // 当前切换器样式名称
        current: 'cur',
        // 是否随机指定默认幻灯图片
        rand: false,
        pre_b: '#left-btn',

        next_b: '#right-btn'
    };

    // settings = $.extend({}, settings, options);
    $.extend(settings, options);

    var $this = $(this),
        index = 0,
        last_index = 3,
        $conbox = $this.find(settings.conbox),
        $contents = $conbox.find(settings.ctag),
        $switcher = $this.find(settings.switcher),
        $stag = $switcher.find(settings.stag),
        Timer,
        contime;

    // 渐变模式预设值
    if (settings.affect == 'fade') {
        $switcher.css({
            'position': 'absolute',
            'z-index': 10
        });
        $.each($contents, function(k, v) {
            if (k === 0) {
                $(this).css({
                    'position': 'absolute',
                    'z-index': 9
                })
            } else {
                $(this).css({
                    'position': 'absolute',
                    'z-index': 1,
                    'opacity': 0
                });
            }
        });
    }

    $this.css('overflow', 'hidden');

    if (settings.affect == 'scrollx') {
        $contents.eq(0).clone().css('float', 'left').appendTo($conbox);
        $this.width($contents.width());
        // $contents建议预设宽度
        $conbox.width(($contents.length + 1) * $contents.width());

        $conbox.css('position', 'relative');
        $contents.css('float', 'left');
    }

    if (settings.affect == 'scrolly') {
        $contents.eq(0).clone().appendTo($conbox);

        $this.height($contents.height());
        // $contents建议预设高度
        $conbox.height(($contents.length + 1) * $contents.height());

        $conbox.css('position', 'relative');
        $contents.css({
            display: 'block'
        });
    }

    // 滚动轮播图模式
    function slide(once) {
        if (index > $contents.length) {
            $conbox.css({'left': 0,'top': 0})
            index = 1;
        }
        if (index == $contents.length) {
            $stag.removeClass(settings.current).eq(0).addClass(settings.current);
            if(settings.affect == 'fade') {
               index = 0;
            }
        }else {
            $stag.removeClass(settings.current).eq(index).addClass(settings.current);
        }
        switch (settings.affect) {
            // 横向滚动
            case 'scrollx':
                if(last_index == 0 && index == ($contents.length - 1) ) {
                    $conbox.finish().css({'left': $contents.length*-$contents.width()});
                }
                if(index == $contents.length) {
                    $conbox.finish().animate({
                        left: -$contents.width() * index
                    }, settings.speed, function() { $conbox.css({'left': 0,'top': 0});});
                }else {
                    $conbox.finish().animate({
                        left: -$contents.width() * index
                    }, settings.speed);
                    
                }
                break;
                // 竖着滚动
            case 'scrolly':
                if(last_index == 0 && index == ($contents.length - 1) ) {
                    $conbox.css({'top': $contents.length*-$contents.height()});
                }
                if(index == $contents.length) {
                    $conbox.finish().animate({
                        top: -$contents.height() * index
                    }, settings.speed, function() { $conbox.css({'left': 0,'top': 0});});
                }else {
                    $conbox.finish().animate({
                        top: -$contents.height() * index
                    }, settings.speed);
                }
                break;
                // 渐变模式
            case 'fade':
                $contents.eq(last_index).finish()
                    .animate({
                        'opacity': 0
                    }, settings.speed / 2)
                    .css('z-index', 1)
                    .end().eq(index).css('z-index', 9).finish()
                    .animate({
                        'opacity': 1
                    }, settings.speed / 2);
                break;
            case 'none':
                $contents.hide().eq(index).show();
                break;
        }
        last_index = index;
        if(last_index == $contents.length) { 
            last_index = 0;
        }
        index++;

        // 随机变幻；
        if (settings.rand) {
            index = Math.floor(Math.random() * $contents.length);
        }
        //判断是否只执行一次。
        if(once) {
            //index = last_index;
        } else {
            clearTimeout(Timer);
            Timer = setTimeout(slide, settings.space);
        }
    };

   
    // 如果设置自动，开始动作
    if (settings.auto) {
        contime = setTimeout(slide, settings.space);
    }

    // 标签事件触发时立即显示当前图片
    $stag.on(settings.trigger, function() {
        _pause();
        index = $(this).index();
        if(last_index == $contents.length - 1 && index == 0) {
            index = $contents.length;
        }
        slide(true);
    });

    // 悬浮时暂停，离开时继续
    $this.mouseenter(_pause);
    $this.mouseleave(_continue);
    // 暂停动画动作
    function _pause() {
        if(Timer) {
            clearTimeout(Timer);
        }
        if(contime) {
            clearTimeout(contime);
        }
    };


    // 继续动作
    function _continue() {

        if(contime) {
            clearTimeout(contime);
        }
        if (settings.auto) {
          contime = setTimeout(slide, settings.space/2);
        }
    };
    // 如果限定在this容器里的可以改为  $(this).find(settings.next_b).click(function(){
    $(settings.next_b).click(function(){
        $conbox.finish();
        clearTimeout(Timer);
        if(contime) {
            clearTimeout(contime);
        }
        index = last_index + 1;
        slide();
    });
    // 如果限定在this容器里的可以改为  $(this).find(settings.pre_b).click(function(){
    $(settings.pre_b).click(function(){
        $conbox.finish();
        clearTimeout(Timer);
        if(contime) {
            clearTimeout(contime);
        }
        index = last_index - 1;
        if(index == -1) {
            index = $contents.length-1;
        }
        slide();
    });

    slide();
}
