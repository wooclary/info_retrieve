function openWin(urls){
	var d=new Date();
	var url = urls +"&t="+d.getTime();
	var windowWidth =  screen.width-155;
	var windowHeight =  screen.height-210;
	v3x.openWindow({
		url : url,
		width : windowWidth,
		height : windowHeight,
		top : 130,
		left : 140,
		resizable: "yes",
		dialogType:'open'
	});
}