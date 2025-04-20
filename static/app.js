// When the form is submitted
document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault(); // Prevent form from submitting normally

    // Get values from the form
    const data = [
        parseFloat(document.getElementById("feature1").value),
        parseFloat(document.getElementById("feature2").value),
        parseFloat(document.getElementById("feature3").value),
        parseFloat(document.getElementById("feature4").value),
        parseFloat(document.getElementById("feature5").value),
        parseFloat(document.getElementById("feature6").value),
        parseFloat(document.getElementById("feature7").value),
        parseFloat(document.getElementById("feature8").value),
        parseFloat(document.getElementById("feature9").value),
        parseFloat(document.getElementById("feature10").value)
    ];
    // Log data to check if it's correct
    console.log("Form Data:", data);

    // Send data to backend for prediction
    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data })
        });

        const result = await response.json();
        
        // Show result on the page
        if (response.ok) {
            document.getElementById('result').innerHTML = `
                <h2>Prediction: ${result.prediction}</h2>
                <p>Meaning: ${result.meaning}</p>
            `;
        } else {
            document.getElementById('result').innerHTML = `
                <h2>Error: ${result.error}</h2>
            `;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `
            <h2>Error: Unable to fetch data from the server</h2>
        `;
    }
});
