document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    fetch('/compare-images', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <h2>Comparison Result</h2>
                <p>Similarity: ${data.similarity.toFixed(2)}%</p>
                <h3>Text from Image 1:</h3>
                <p>${data.text1}</p>
                <h3>Text from Image 2:</h3>
                <p>${data.text2}</p>
            `;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    });
});
