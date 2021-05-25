/*this is the function for the carousel */
var pictureIndex = 1;
pictureShow(pictureIndex);

function nextPicture(n) {
  pictureShow(pictureIndex += n);
}

function pictureShow(n) {
  var i;
  var x = document.getElementsByClassName("pictureSlides");
  if (n > x.length) {pictureIndex = 1}
  if (n < 1) {pictureIndex = x.length} ;
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  x[pictureIndex-1].style.display = "block";
}

