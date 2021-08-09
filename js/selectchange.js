
document.addEventListener("DOMContentLoaded", function(event) { 
  //do work



const selectElement = document.querySelector('.navi-change-chapter');
selectElement.addEventListener('change', (event) => {
curr = window.location.href.split("/")[window.location.href.split("/").length-2]
curr = curr.replaceAll(/[\/\\\:\*\?\"\<\>\|\.]/gi,"_")
newr = event.target.value.replaceAll(/[\/\\\:\*\?\"\<\>\|\.]/gi,"_")
  newurl = window.location.href.replace(curr,newr)
console.log(newurl)
window.location.href = newurl;
});
const s = document.querySelectorAll('.navi-change-chapter')[1];

s.addEventListener('change', (event) => {
curr = window.location.href.split("/")[window.location.href.split("/").length-2]
curr = curr.replaceAll(/[\/\\\:\*\?\"\<\>\|\.]/gi,"_")
newr = event.target.value.replaceAll(/[\/\\\:\*\?\"\<\>\|\.]/gi,"_")
  newurl = window.location.href.replace(curr,newr)
console.log(newurl)
window.location.href = newurl;
});

});
