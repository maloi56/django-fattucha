document.getElementById("get_calories").addEventListener("click", function () {
    const deficitKcal = parseFloat(document.getElementById("wanted_kkal").value);
    const days = parseInt(document.getElementById("wanted_days").value);

    if (isNaN(deficitKcal) || isNaN(days)) {
      alert("Пожалуйста, введите числовые значения.");
      return;
    }
    const totalDeficit = deficitKcal * days;
    const weightLossKg = totalDeficit / 7700;

    const resultElement = document.getElementById("result");
    resultElement.innerHTML = `
      <div class="mt-3 alert alert-success">
        За ${days} дней с дефицитом в ${deficitKcal} ккал, вы потеряете примерно ${weightLossKg.toFixed(2)} кг жира.
      </div>
    `;
  });