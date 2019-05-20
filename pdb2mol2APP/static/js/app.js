$("#demo-upload").dropzone({
  url: "handle-upload.php",
  maxFiles: 20,
  maxFilesize: 5120,
  acceptedFiles: ".pdb"
});