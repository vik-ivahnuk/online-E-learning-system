function copy() {
      var copyText = document.getElementById("idCourse");

      copyText.select();
      copyText.setSelectionRange(0, 99999);
      navigator.clipboard.writeText(copyText.value);
}