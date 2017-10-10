function strong(){
  var textarea=document.querySelector('.body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  var selection=alltext.substring(start,end);
  if (selection.length==0) {
    var newtext=alltext.substring(0,start)+'*b*'+alltext.substring(end,alltext.length);
  } else {
    var newtext=alltext.substring(0,start)+'*b*'+selection+'*b*'+alltext.substring(end,alltext.length);
  };
  textarea.value=newtext;
};
function em(){
  var textarea=document.querySelector('.body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  var selection=alltext.substring(start,end);
  if (selection.length==0) {
    var newtext=alltext.substring(0,start)+'*i*'+alltext.substring(end,alltext.length);
  } else {
    var newtext=alltext.substring(0,start)+'*i*'+selection+'*i*'+alltext.substring(end,alltext.length);
  };
  textarea.value=newtext;
};
function u(){
  var textarea=document.querySelector('.body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  var selection=alltext.substring(start,end);
  if (selection.length==0) {
    var newtext=alltext.substring(0,start)+'*u*'+alltext.substring(end,alltext.length);
  } else {
    var newtext=alltext.substring(0,start)+'*u*'+selection+'*u*'+alltext.substring(end,alltext.length);
  };
  textarea.value=newtext;
};
function autoImg(input){
  /* hide current input, create new one */
  /* var newInput=input.cloneNode(true); */
  var newInput=document.createElement('input');
  newInput.setAttribute('id','file');
  newInput.setAttribute('name','file');
  newInput.setAttribute('type','file');
  newInput.setAttribute('onchange','autoImg(this)');
  input.hidden=true;
  input.after(newInput);
  /* get textarea */
  var textarea=document.querySelector('.body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  /* get filename */
  var fullPath=input.value;
  var filename=fullPath.split(/[/\\]/)[fullPath.split(/[/\\]/).length-1];
  /* var filename=filename.split('.')[0];*/
  /* set textarea */
  var newtext=alltext.substring(0,start)+'*img*'+filename+'*img*'+alltext.substring(end,alltext.length);
  textarea.value=newtext;
};
function highlightLabel(el){
  return;
  var checkbox = el.querySelector('input');
  if (checkbox.checked) {
    el.style.background = 'red';
  } else {
    el.style.background = 'none';
  };
};
