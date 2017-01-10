function setTab(n,url){
	var tli=document.getElementById("menu1").getElementsByTagName("li");
 	for(i=0;i<tli.length;i++){
  		if(i==n){
			setCookie("show_item",n,1);
  		}
 	}
 	if(url!='')
 		window.location.href=url;
}
function setCookie(sName,sValue,expireHours) {
	var cookieString = sName + "=" + escape(sValue);

	if (expireHours>0) {
		var date = new Date();
		date.setTime(date.getTime + expireHours * 3600 * 1000);
		cookieString = cookieString + "; expire=" + date.toGMTString();
	}
	document.cookie = cookieString;
}
	

function getCookie(sName) {
	var aCookie = document.cookie.split("; ");
	for (var j=0; j < aCookie.length; j++){
		var aCrumb = aCookie[j].split("=");
		if (escape(sName) == aCrumb[0])
		  return unescape(aCrumb[1]);
	}
	return null;
}
window.onload= function(){
	var n = getCookie("show_item");
	//setCookie("show_item",0,1);
	if(n!=null && n>=0 && n<7 && document.getElementById("menu1") !=null&& document.getElementById("menu1")!='undefined'){
		var tli=document.getElementById("menu1").getElementsByTagName("li");
		for(i=0;i<tli.length;i++){
    		tli[i].className=i==n?"active":"";
 		}
	}
}

function ShowfdCs() {
	if (document.getElementById("fdCs").style.display == "none") {
		document.getElementById("fdCs").style.display = "block";
	} else {
		document.getElementById("fdCs").style.display = "none";
	}
}
function _frm_submit(frm, ac) {

	frm.action = ac;
	frm.submit();
}
function _frm_submit_check(frm, ac,msg) {
	frm.action = ac;

	Delete_click(frm,'idArray',msg);
}

function CheckAll(frm,checkAllBox) {
	var ChkState = checkAllBox.checked;
	for (i = 0; i < frm.length; i++) {
		e = frm.elements[i];
		if (e.type == "checkbox" && e.name.indexOf("checkItem") != -1) {
			e.checked = ChkState;
		}
	}
	if (ChkState == true) {
		frm.BtnDel.disabled = false;
	} else {
		frm.BtnDel.disabled = true;
	}
}
function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}

 function windowopen(openurl,width,height)
{
	var windowwidth;
	var windowheight;
	
	if (parseInt(width)>800)
	{
		windowwidth = 810;
		windowheight = 550;
	}
	else
	{
		windowwidth = parseInt(width)*0.9;
		windowheight = parseInt(height)*0.9;
	}

	var windowleft = parseInt((width - windowwidth)/2);
	var windowtop = parseInt((height - windowheight)/2);
	var pagename = Math.random();
	pagename = pagename.toString();
	pagename = pagename.substr(2);
	window.open(openurl,pagename,'top=' + windowtop + ',left=' + windowleft + ',width='+(windowwidth)+',height= '+ windowheight + ',resizable=0,scrollbars=0,status=no,toolbar=no,location=no,menubar=no,titlebar=no,dependent')
	return false;
}

function SeletAll(strCheckBoxName)
{	
	
	SelectAction(strCheckBoxName,true);
}
		
function ClearAll(strCheckBoxName)
{
	SelectAction(strCheckBoxName,false);
}

function SelectAction(strCheckBoxName,straction)
{
	if(document.all(strCheckBoxName)==null)
		return false;
	if (typeof(document.all(strCheckBoxName).checked)=="undefined")
	{
		if(typeof(document.all(strCheckBoxName))!="undefined"){
		
			for (i = 0 ; document.all(strCheckBoxName).length > i ; i ++)
			{
				document.all(strCheckBoxName)[i].checked = straction;
			}
		}
	}
	 else
	 {
	  	document.all(strCheckBoxName).checked=straction;
	 }
}

function add(from,to)
{
	var allbooth = document.all(from);
	var newselect = document.all(to);
	var oNewNode;
	var newoption;
	if(newselect.children.length!=0){
		for(i =0;i<allbooth.children.length;i++)
		{
		if(allbooth.children[i].selected)
			for(j=0;j<newselect.children.length;j++)
				if(allbooth.children[i].value==newselect.children[j].value)
				{	alert(allbooth.children[i].innerText+" have already selected!");
					return false;
				}
		}
	}
	for(i =0;i<allbooth.children.length;i++)
	{
	 	if(allbooth.children[i].selected)
	 	{
	 		newoption = document.createElement("option");
		 	newoption.value=allbooth.children[i].value;
		 	newoption.innerText=allbooth.children[i].innerText;
	   		newselect.appendChild(newoption);
	   		newoption.selected=true;
   		}
   	}
	return false;
}

function remove(removeobj)
{
	var newselect = document.all(removeobj);
	var obj = new Array();
	var k = 0;
	
	for(i =0;i<newselect.childNodes.length;i++){
	 	if(newselect.childNodes[i].selected){
  			obj[k] = newselect.childNodes[i];
  			k++;
	  	}
	  }
  	for(i=0;i<k;i++)
  		newselect.removeChild(obj[i]);
  	
	return false;
}
