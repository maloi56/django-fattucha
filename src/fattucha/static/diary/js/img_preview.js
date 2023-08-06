document.getElementById('image-input').addEventListener('change', function(event) {
  var input = event.target;
  var reader = new FileReader();

  reader.onload = function() {
    var imagePreview = document.getElementById('image-preview');
    imagePreview.src = reader.result;
  };

  reader.readAsDataURL(input.files[0]);
});
