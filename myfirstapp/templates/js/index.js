// static/myapp/js/script.js
document.addEventListener("DOMContentLoaded", function() {
    var loadButton = document.getElementById("carregarXlsx");
    var generateButton = document.getElementById("gerarXml");

    loadButton.addEventListener("click", function() {
        // Your Python code to handle loading .xlsx files can go here
        console.log("Load button clicked");
        window.alert("carregar");
    });

    generateButton.addEventListener("click", function() {
        // Your Python code to handle generating .xml files can go here
        console.log("Generate button clicked");
        window.alert("gerar");
    });
});

gerarXml