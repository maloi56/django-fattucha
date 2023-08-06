const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const csrftoken = getCookie("csrftoken");

const ratingButtons = document.getElementById('like_id');


ratingButtons.addEventListener('click', event => {
  // Получаем значение рейтинга из data-атрибута кнопки
  const recipeId = parseInt(event.target.dataset.recipe)
  const ratingSum = document.querySelector('.rating-sum');
  // Создаем объект FormData для отправки данных на сервер
  const formData = new FormData();
  // Добавляем id статьи, значение кнопки
  formData.append('recipe_id', recipeId);
  fetch("/like/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      "X-Requested-With": "XMLHttpRequest",
    },
    body: formData
  }).then(response => response.json())
    .then(data => {
      // Обновляем значение на кнопке
      ratingSum.textContent = data.likes;
      if (ratingButtons.className == "fa-regular fa-heart fa-lg") {
        ratingButtons.className = "fa-solid fa-heart fa-lg"
      }
      else {
        console.log('hui')
        ratingButtons.className = "fa-regular fa-heart fa-lg"
      }
    })
    .catch(error => console.error(error));

});