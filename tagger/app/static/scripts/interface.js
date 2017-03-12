/**
 * Created by Shawn on 2017/3/6.
 */
$(document).ready(function(){
        $("a.item").click(function() {
            var current = $(this);
            $("iframe#insert-iframe").attr('src', "/panel?filename=" + current.text());
        });
});