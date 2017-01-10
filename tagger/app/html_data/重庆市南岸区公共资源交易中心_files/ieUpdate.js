/**
* Added by jerry for resolve ie upgrade activity activeX control issue.
*
* param: url -- activeX's resource address
*        w   -- object's width
*        h   -- object's height
*
* call function like this:
*		insertFlash("index.swf", 600, 350);
*/
function closeWindow()
{  
   window.inner=new Object();
   window.close();
}

function insertFlash(url, w, h)
{
	 document.write('<div>');
	 document.write('<object width="'+ w +'" height="'+ h +'" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=7,0,0,0">'); 
	 document.write('<param name="movie" value="'+ url +'">');
	 document.write('<param name="wmode" value="transparent">');
	 document.write('<param name="quality" value="high">');
	 document.write('<embed width="'+ w +'" height="'+ h +'" src="'+ url +'" quality="high" wmode="transparent" type="application/x-shockwave-flash" plugspace="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash"></embed>');
	 document.write('</object>');
	 document.write('</div>');
}