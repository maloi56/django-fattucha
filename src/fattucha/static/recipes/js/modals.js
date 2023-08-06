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
const input = document.getElementById('food-search-input');
let filteredArr = [];
const box = document.getElementById('box');
const clearIcon = document.querySelector('.clear-icon');
let totalForms = document.querySelector("#id_ingredients-TOTAL_FORMS")

function afterDelayLogic(value) {
  fetch(`/get_products/?q=${value}`, {
    method: 'GET',
    headers: {
      'X-CSRFToken': csrftoken,
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then(response => response.json())
    .then(data => {
      filteredArr = data.products.filter(product =>
        product['name'].toLowerCase().includes(value.toLowerCase())
      );

      if (filteredArr.length > 0 && input.value !== '') {
        const fragment = document.createDocumentFragment();

        filteredArr.forEach(product => {
          const card = document.createElement('div');
          card.classList.add('card', 'mb-3', 'text-center');
          card.style.padding = '10px 0';
          card.setAttribute('data-bs-toggle', 'modal');
          card.setAttribute('data-bs-target', '#addFoodModal');
          card.setAttribute('data-bs-dismiss', 'modal');
          card.setAttribute('data-bs-config', JSON.stringify({
            "calories": product['calories'],
            "protein": product['protein'],
            "fat": product['fat'],
            "carbs": product['carbohydrates'],
            "name": product['name'],
            "brand": product['brand'],
            "id": product['id']
          }));
    
          const foundFood = document.createElement('div');
          foundFood.classList.add('found_food');
    
          const p = document.createElement('p');
          p.style.lineHeight = '2';
          p.textContent = `${product['name']}\n${product['brand'] !== null ? product['brand'] + ',' : ''} 100г = ${product['calories']} ккал`;
    
          foundFood.appendChild(p);
          card.appendChild(foundFood);
          fragment.appendChild(card);
        });
    
        box.appendChild(fragment);
      } else if (input.value !== '') {
        box.textContent = "Ничего не найдено...";
      } else {
        box.textContent = "";
      }
    })
    .catch(error => console.error(error));

  console.log(value);
}

input.addEventListener('input', (e) => {
  clearIcon.style.display = input.value ? 'block' : 'none';
  box.textContent = "";
  if (!input.value) {
    box.innerHTML = '<b></b>';
  }
  // Clear filteredArr since it's not used outside this function
  filteredArr = [];
  // Debounce the function call by 500 milliseconds
  clearTimeout(input.timeout);
  input.timeout = setTimeout(afterDelayLogic, 300, input.value);
});

clearIcon.addEventListener('click', () => {
  input.value = '';
  box.textContent = "";
});

const save_changes_button = document.getElementById('save-changes_food-button');
const changeModal = document.getElementById('changeFoodSettingsModal');
let p_for_change = {};
let changed_weight = 0;

if (changeModal) {
  changeModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const recipient = button.getAttribute('data-bs-config');
    p_for_change = JSON.parse(recipient);
    const modalBodyInput = document.getElementById('change_weight');

    modalBodyInput.value = p_for_change.weight;

    const caloriesCell = document.getElementById("calories_1");
    const proteinCell = document.getElementById("protein_1");
    const fatCell = document.getElementById("fat_1");
    const carbsCell = document.getElementById("carbs_1");

    caloriesCell.textContent = parseInt(p_for_change.recipient.calories / 100 * p_for_change.weight) + ' ккал';
    proteinCell.textContent = "Белки - " + (modalBodyInput.value * p_for_change.recipient.protein / 100).toFixed(2) + 'г';
    fatCell.textContent = "Жиры - " + (modalBodyInput.value * p_for_change.recipient.fat / 100).toFixed(2) + 'г';
    carbsCell.textContent = "Углеводы - " + (modalBodyInput.value * p_for_change.recipient.carbs / 100).toFixed(2) + 'г';

    modalBodyInput.addEventListener('input', (e) => {
      caloriesCell.textContent = parseInt(modalBodyInput.value * p_for_change.recipient.calories / 100) + ' ккал';
      proteinCell.textContent = "Белки - " + (modalBodyInput.value * p_for_change.recipient.protein / 100).toFixed(2) + 'г';
      fatCell.textContent = "Жиры - " + (modalBodyInput.value * p_for_change.recipient.fat / 100).toFixed(2) + 'г';
      carbsCell.textContent = "Углеводы - " + (modalBodyInput.value * p_for_change.recipient.carbs / 100).toFixed(2) + 'г';
      console.log(e)

      changed_weight = modalBodyInput.value;
      console.log(changed_weight)
    });
  });

  save_changes_button.addEventListener("click", function () {
    const formset_weight = document.getElementById(`id_ingredients-${p_for_change.formset_id}-weight`);
    formset_weight.value = changed_weight;
    const formset_visible = document.getElementById(`id_ingredients-${p_for_change.formset_id}-visible`);
    formset_visible.value = `${changed_weight} г ${p_for_change.recipient.name}`;

    formset_visible.setAttribute("data-bs-config", JSON.stringify({
      "weight": changed_weight,
      "formset_id": p_for_change.formset_id,
      "recipient": p_for_change.recipient
    }));
  });
}

const searchModal = document.getElementById('searchFoodModal');
if (searchModal) {
  searchModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const recipient = button.getAttribute('data-bs-config');
    const p = JSON.parse(recipient);
    const input = document.getElementById('food-search-input');
    input.value = '';
    box.textContent = "";
  });
}

let p = {};
const myModal = new bootstrap.Modal(document.getElementById('addFoodModal'));
const addFood = document.getElementById('addFoodModal');
let add_recipient = "";

if (addFood) {
  addFood.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const recipient = button.getAttribute('data-bs-config');
    add_recipient = recipient;
    p = JSON.parse(recipient);

    const input = document.getElementById('food-weight');
    input.value = '';

    const caloriesCell = document.getElementById("calories");
    const proteinCell = document.getElementById("protein");
    const fatCell = document.getElementById("fat");
    const carbsCell = document.getElementById("carbs");

    caloriesCell.textContent = 0 + ' ккал';
    proteinCell.textContent = "Белки - " + 0 + 'г';
    fatCell.textContent = "Жиры - " + 0 + 'г';
    carbsCell.textContent = "Углеводы - " + 0 + 'г';

    input.addEventListener('input', (e) => {
      caloriesCell.textContent = parseInt(input.value * p.calories / 100) + ' ккал';
      proteinCell.textContent = "Белки - " + (input.value * p.protein / 100).toFixed(2) + 'г';
      fatCell.textContent = "Жиры - " + (input.value * p.fat / 100).toFixed(2) + 'г';
      carbsCell.textContent = "Углеводы - " + (input.value * p.carbs / 100).toFixed(2) + 'г';
    });
  });

  const formsetContainer = document.getElementById("ingredients-formset");
  const addButton = document.getElementById("save-food-button");
  addButton.addEventListener("click", function () {
    const input = document.getElementById('food-weight');
    if (!input.value.trim() || input.value <= 0) {
      alert('Некорректное значение веса!');
    } else {
      const formIdx = parseInt(totalForms.value)
      const formsetItem = document.createElement('div');
      formsetItem.classList.add('formset-item');

      formsetItem.innerHTML = `
        <div class="row mb-2 justify-content-center">
          <div class="col-md-8">
            <label for="id_ingredients-${formIdx}-product">Ингредиент:</label>
            <input type="text" id='id_ingredients-${formIdx}-visible' class="form-control" value='${input.value} г ${p.name}' data-bs-toggle="modal"
                 data-bs-target="#changeFoodSettingsModal"
                 data-bs-config='{
                   "weight": "${input.value}",
                   "formset_id": "${formIdx}",
                   "recipient" : ${add_recipient}
                 }' readonly>
            <input type="hidden" name="ingredients-${formIdx}-product" id="id_ingredients-${formIdx}-product" value=${p.id}>
            <input type="hidden" class="form-control" name="ingredients-${formIdx}-weight" id="id_ingredients-${formIdx}-weight" value=${input.value} readonly>
          </div>
          <div class="col-md-2 d-flex align-items-end">
            <button type="button" class="btn btn-danger mt-3 w-100 remove-formset-item">Удалить</button>
          </div>
        </div>`;

      formsetContainer.appendChild(formsetItem);
      totalForms.value = formIdx + 1
      myModal.hide();
    }
  });

  formsetContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-formset-item')) {
      const formset = e.target.closest('.formset-item');
      totalForms.value = parseInt(totalForms.value) - 1
      formset.remove();
    }
  });
}

function validateFormset() {
  const ingredientFormsetItems = document.querySelectorAll('.formset-item');
  const minIngredientsCount = 3;

  if (ingredientFormsetItems.length < minIngredientsCount) {
    alert(`Добавьте как минимум ${minIngredientsCount} ингредиента`);
    return false;
  }

  return true;
}

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('recipe-form');

  form.addEventListener('submit', function (event) {
    if (!validateFormset()) {
      event.preventDefault();
    }
  });
});
