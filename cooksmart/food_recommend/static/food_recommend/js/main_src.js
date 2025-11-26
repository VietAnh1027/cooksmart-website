async function sendQuery(){
    const text = document.getElementById("user-input").value.trim();
    const limit = document.getElementById("result-count").value;
    alert("Bạn đã nhấn tìm kiếm!")
    const response = await fetch(`/search_api/?q=${encodeURIComponent(text)}&limit=${limit}`);
    const data = await response.json();
    console.log(data)
    const resultBox = document.getElementById("results");
    resultBox.innerHTML = "";

    data.forEach(item => {
        ingredientsList = item.ingredients.map(ing => `<li>${ing}</li>`).join("");
        const card = document.createElement("div");
        card.className = "result-card";
        card.innerHTML = `
            <h3>${item.title}</h3>
            <p><strong>Ingredients:</strong></p>
            <ul>${ingredientsList}</ul>
            <p><strong>How to cook:</strong> ${item.directions}</p>
        `;
        resultBox.appendChild(card);
    });
}