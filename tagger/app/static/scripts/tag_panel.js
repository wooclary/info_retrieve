(function ($) {
	var find_path = function (node) {
		var parent = $(node).parent()[0];
		if (node.tagName.toLowerCase() == 'html' || !parent) {
			return {p1: 'html', p2: 'html', p3: 'html'};
		}
		var tag = node.tagName.toLowerCase();
		var path = tag;
		var classattr = $(node).attr('class');
		if (classattr !== undefined) {
			path += '[class=\'' + classattr + '\']';
			var classes = node.classList;
			for (var cls of classes) {
				tag += '.' + cls;
			}
		} else {
			path += ':not([class])';
		}
		var common_sel = (classattr==undefined || node.classList.length<2)?path:tag;
		var pret = find_path(parent);
		return {
			p1: pret.p1 + ' > ' + path,
			p2: pret.p2 + ' > ' + tag,
			p3: pret.p3 + ' > ' + common_sel
		};
	};
	$(function () {
		var current = {};
		$('body').mousemove(function (event) {
			if (current.target == event.target) {
				return;
			}
			current.target = event.target
			$('.wbzz6-highlight').each(function () {
				$(this).removeClass('wbzz6-highlight');
				if (/^\s*$/.test($(this).attr('class'))) {
					$(this).removeAttr('class');
				}
			});
			$('[class]').each(function () {
				var classstr = $(this).attr('class').split(/\s+/).sort().join(' ');
				$(this).attr('class', classstr);
			});
			var new_path = find_path(current.target);
			$.extend(current, new_path);
			$(parent.document).find('#current_label_sequence').text(new_path.p2);
			$(current.p1).addClass('wbzz6-highlight');
		});
		// disable all anchor click event
		$('a').click(function(evt) { evt.preventDefault(); });
		$('body').click(function () {
			// TODO modify to AJAX request
			alert(current.p2);
			var sequence = current.p2;
			var sel = current.p1;
			var common = current.p3;
			var path = $('#insert-iframe').attr("src");
			$.ajax({
				url: path,
				type: 'POST',
				data: JSON.stringify({
					label_sequence: sequence,
					selector: sel,
					common: common
				}),
				contentType: 'application/json; charset=utf-8',
				dataType: 'json',
				async: false,
                cache: false,
				success: function(msg) {
                    if(msg.status == 200){
                        alert("save success");
                    } else {
                        alert("save fail")
                    }
				}
			});
		});
		// 文档加载完成时，向后端请求已存好的规则
		$(document).ready(function() {
                var path = '/rule' + location.search;
                $.getJSON(path, function (data, status) {
                    if (status == 'success') {
                    	if (data.is_rec==false) {
                            var selector = data.sel;
                            $(selector).attr('data-mark', data.is_rec);
                        }
                        else{
                    		var selector = data.seq;
                    		$(selector).attr('data-mark', data.is_rec);
						}
                    }
                });
            }
		);
	});
})(wbzz6_jq);
