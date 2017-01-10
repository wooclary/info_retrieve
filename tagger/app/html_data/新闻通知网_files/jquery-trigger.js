var $DateTab = 
{
    ToggleClass: function (ele) {
        $(ele).parent().parent().find("a").each(function () {
            if ($(this).hasClass("on")) {
                $(this).toggleClass("on");
            }
        });
        $(ele).toggleClass("on");
    }
}

var $Page =
{
    InitPage: function () {
        if (typeof $("#wrap")[0] != "undefined") {
            var minWidth = 1000;
            $("#wrap").css("width", minWidth + "px");
            if ($(window).width() < minWidth) {
                $("#wrap").css("left", "0");
                $("#wrap").css("margin-left", "0");
            }
            else {
                $("#wrap").css("left", "50%");
                $("#wrap").css("margin-left", "-500px");
            }
        }
    }
}