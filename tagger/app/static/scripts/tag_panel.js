(function () {
	var $ = window.wbzz6_jq;
	var current_elem;
	var bind_all = function (node) {
		$(node).each(function () {
			this.addEventListener('mousemove', function () {
				current_elem = this;
			}, true);
		});
		$(node).children().each(function () {
			bind_all(this);
		});
	};
	var find_path = function (node) {
		var rs = {};
		rs['html'] = node.outerHTML;
		var r_path = function (node) {
			var parent = $(node).parent()[0];
			if (node.tagName.toLowerCase() == 'html' || !parent) {
				return 'html';
			} else {
				return r_path(parent) + ' > ' + node.tagName;
			}
		};
		rs['path'] = r_path(node);
		return rs;
	};
	$(function () {
		$('body').each(function () {
			bind_all(this);
		});
		$('body').mousemove(function () {
			$('.wbzz6-highlight').removeClass('wbzz6-highlight');
			$(find_path(current_elem).path).addClass('wbzz6-highlight');
		});
		$('body').click(function () {
			// TODO modify to AJAX request
			var sequence = find_path(current_elem).path;
			var path = $('#insert-iframe').attr("src");
			$.ajax({
				url: path,
				type: 'POST',
				data: JSON.stringify({
					label_sequence: sequence
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
	});
	
})();
