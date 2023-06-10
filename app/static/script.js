

function getPolarityValue() {
    fetch('/get_polarity')
        .then(response => response.text())
        .then(data => {
            document.getElementById('output1').innerHTML = data;
        });
}

function getPolarityValue_gpt4all() {
    fetch('/get_polarity_gpt4all')
        .then(response => response.text())
        .then(data => {
            document.getElementById('output2').innerHTML = data;
        });
}

window.onload = function () {
    // console.log("inside on load calling priority value");
    getPolarityValue();
    // console.log("called getPolarityValue, about to call gpt4all");
    getPolarityValue_gpt4all();
    // console.log("done");
};


