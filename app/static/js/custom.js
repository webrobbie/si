function strong(){  var textarea=document.querySelector('#body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  var selection=alltext.substring(start,end);
  var newtext=alltext.substring(0,start)+'<strong>'+selection+'</strong>'+alltext.substring(end,alltext.length);
  textarea.value=newtext;
}
function em(){
  var textarea=document.querySelector('#body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  var selection=alltext.substring(start,end);
  var newtext=alltext.substring(0,start)+'<em>'+selection+'</em>'+alltext.substring(end,alltext.length);
  textarea.value=newtext;
}
function u(){
  var textarea=document.querySelector('#body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  var selection=alltext.substring(start,end);
  var newtext=alltext.substring(0,start)+'<u>'+selection+'</u>'+alltext.substring(end,alltext.length);
  textarea.value=newtext;
}
function autoImg(input){
  var row=input.parentNode.parentNode;
  var newRow=row.cloneNode(true);
  row.hidden=true;
  row.parentNode.appendChild(newRow);
  var textarea=document.querySelector('#body');
  var start=textarea.selectionStart;
  var end=textarea.selectionEnd;
  var alltext=textarea.value;
  /* local fake path vs online */
  /*if (input.value.search('/')) {*/
    /*var upload_folder='static/upload/';*/
    /*var filename=input.value.split('\\')[2];*/
  /*} else {*/
    /*var upload_folder='/static/upload/';*/
    /*var filename=input.value;*/
  /*}*/
  var filename=input.value;
  var newtext=alltext.substring(0,start)+"<img src='/static/upload/"+filename+"' alt='"+filename+"' class='img-fluid'>"+alltext.substring(end,alltext.length);
  textarea.value=newtext;
}
function test(el){
  alert(document.querySelectorAll('input[type=file]').length-1);
}
