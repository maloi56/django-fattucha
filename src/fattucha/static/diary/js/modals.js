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
const rep_type_input = document.getElementById('rep_type_input');
const box = document.getElementById('box');

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
      box.innerHTML = '';

      filteredArr = data.products.filter(product =>
        product['name'].toLowerCase().includes(value.toLowerCase())
      );

      if (filteredArr.length > 0 && value !== '') {
        box.innerHTML = filteredArr
          .map(
            product => `
                <div class="card mb-3 text-center" style="padding: 10px 0;"
                         data-bs-toggle="modal"
                         data-bs-target="#addFoodModal" data-bs-dismiss="modal"
                         data-bs-config='{
                          "calories": ${product['calories']},
                          "protein": ${product['protein']},
                          "fat": ${product['fat']},
                          "carbs": ${product['carbohydrates']},
                          "id": ${product['id']},
                          "report": ${report_id},
                          "rep_id": ${rep_type_input.value}}'>
                        <div class="found_food">
                            <p style="line-height: 2;">
                            ${product['name']}<br>
                            ${product['brand'] != null ? product['brand'] + ',' : ''}
                             100г = ${product['calories']} ккал
                             </p>
                        </div>
                    </div>`
          )
          .join('');
      } else if (input.value !== '') {
        box.innerHTML = '<b>Ничего не найдено...</b>';
      } else {
        box.innerHTML = '<b></b>';
      }
    })
    .catch(error => console.error(error));

  console.log(value);
}

input.addEventListener('input', e => {
  console.log('Нажата клавиша:', e.key);

  // Clear the box content if the input value is empty
  if (!input.value) {
    box.innerHTML = '<b></b>';
  }

  // Clear filteredArr since it's not used outside this function
  filteredArr = [];

  // Debounce the function call by 500 milliseconds
  clearTimeout(input.timeout);
  input.timeout = setTimeout(afterDelayLogic, 300, input.value);
});

function updateCellText(modalBodyInput, p) {
  const caloriesCell = document.getElementById('calories_1');
  const proteinCell = document.getElementById('protein_1');
  const fatCell = document.getElementById('fat_1');
  const carbsCell = document.getElementById('carbs_1');

  caloriesCell.textContent = parseInt(p.calories / 100 * modalBodyInput.value) + ' ккал';
  proteinCell.textContent = 'Белки - ' + (modalBodyInput.value * p.protein / 100).toFixed(2) + 'г';
  fatCell.textContent = 'Жиры - ' + (modalBodyInput.value * p.fat / 100).toFixed(2) + 'г';
  carbsCell.textContent = 'Углеводы - ' + (modalBodyInput.value * p.carbs / 100).toFixed(2) + 'г';
}

const changeModal = document.getElementById('changeFoodSettingsModal');
if (changeModal) {
  changeModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const recipient = button.getAttribute('data-bs-config');
    const p = JSON.parse(recipient);
    const modalBodyInput = document.getElementById('change_food_weight');
    modalBodyInput.value = p.weight;

    // Update the cell text when the input value changes
    modalBodyInput.addEventListener('input', e => {
      console.log(e);
      updateCellText(modalBodyInput, p);
    });

    updateCellText(modalBodyInput, p);

    const report_type_input = document.getElementById('change_report_type');
    const food_id_input = document.getElementById('food_id');
    const product_input = document.getElementById('change_product_id');
    food_id_input.value = p.id;
    product_input.value = p.product;

    const link = document.getElementById('remove_food');
    let parts = link.href.split('/');
    parts[parts.length - 1] = p.id;
    let newUrl = parts.join('/');
    link.href = newUrl;

    const form = document.getElementById('change_form');
    parts = form.action.split('/');
    parts[parts.length - 1] = p.id;
    newUrl = parts.join('/');
    form.action = newUrl;

    report_type_input.value = p.rep_id;
  });
}

const searchModal = document.getElementById('searchFoodModal');
if (searchModal) {
  searchModal.addEventListener('show.bs.modal', event => {
    const rep_input = document.getElementById('rep_type_input');
    const button = event.relatedTarget;
    const recipient = button.getAttribute('data-bs-config');
    const p = JSON.parse(recipient);
    rep_input.value = p.rep_type;
    input.value = '';
    box.innerHTML = '<b></b>';
  });
}

const addFood = document.getElementById('addFoodModal');
if (addFood) {
  addFood.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const recipient = button.getAttribute('data-bs-config');
    const p = JSON.parse(recipient);

    const input = document.getElementById('food-weight');
    input.value = '';

    const report_type_input = document.getElementById('report_type');
    report_type_input.value = p.rep_id;

    const id_product_input = document.getElementById('product_id');
    id_product_input.value = p.id;

    const id_report_input = document.getElementById('report');
    id_report_input.value = p.report;

    const caloriesCell = document.getElementById('calories');
    const proteinCell = document.getElementById('protein');
    const fatCell = document.getElementById('fat');
    const carbsCell = document.getElementById('carbs');

    caloriesCell.textContent = '0 ккал';
    proteinCell.textContent = 'Белки - 0г';
    fatCell.textContent = 'Жиры - 0г';
    carbsCell.textContent = 'Углеводы - 0г';

    // Update the cell text when the input value changes
    input.addEventListener('input', e => {
      console.log(e);
      caloriesCell.textContent = parseInt(input.value * p.calories / 100) + ' ккал';
      proteinCell.textContent = 'Белки - ' + (input.value * p.protein / 100).toFixed(2) + 'г';
      fatCell.textContent = 'Жиры - ' + (input.value * p.fat / 100).toFixed(2) + 'г';
      carbsCell.textContent = 'Углеводы - ' + (input.value * p.carbs / 100).toFixed(2) + 'г';
    });
  });
}
