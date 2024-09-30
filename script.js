document
  .getElementById("uploadForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log("hello");

    // Create FormData object
    let formData = new FormData();
    formData.append("pdfFile", document.getElementById("pdfFile").files[0]);

    console.log(document.getElementById("pdfFile").files[0]);
    document.getElementById("statusMessage").textContent = "Processing...";

    // Send the form data using fetch
    const res = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
      // Do not set 'Content-Type' header manually with FormData
    });
    const data = await res.json();
    // .then((response) => {
    //   if (!response.ok) {
    //     // Check if the response status is not OK
    //     throw new Error("Network response was not ok.");
    //   }
    //   console.log("response received")
    //   response.json(); // Parse JSON response
    // })
    // .then((data) => {
    console.log(data);
    document.getElementById("statusMessage").textContent =
      "Processing complete!";

    if (data.error) {
      document.getElementById(
        "statusMessage"
      ).textContent = `Error: ${data.error}`;
    } else {
      let resultsDiv = document.getElementById("results");
      resultsDiv.innerHTML = "<h2>Available Reports:</h2>";

      data.files.forEach((file) => {
        let link = document.createElement("a");
        link.href = `/download/${file}`;
        link.textContent = `Download ${file}`;
        link.style.display = "block";
        resultsDiv.appendChild(link);
      });
    }
  });
