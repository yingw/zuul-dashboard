function copy_to_clipboard(selector) {
    var dummy = document.createElement("input");
    document.body.appendChild(dummy);
    dummy.setAttribute('value', selector);
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
}
