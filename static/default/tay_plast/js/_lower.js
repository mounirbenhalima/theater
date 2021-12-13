var input = document.getElementsByTagName("input")[0] // just your input element

input.oninput = function() {
  input.value = input.value.toLowerCase()
}