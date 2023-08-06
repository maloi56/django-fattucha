const addStepButton = document.getElementById("add-step-btn");
const stepsTotalForms = document.querySelector("#id_steps-TOTAL_FORMS");
const stepFormsetContainer = document.getElementById("steps-formset");

const ZeroImageInput = document.getElementById(`id_steps-0-image`);
const ZeroImagePreview = document.getElementById(`ingredient-preview-0`);
ZeroImageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            ZeroImagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});


function createStepForm(StepformIdx) {
    const stepsFormsetItem = document.createElement('div');
    stepsFormsetItem.classList.add('step-formset-item');
    stepsFormsetItem.innerHTML = `
        <div class="row mb-2 align-items-center mt-3">
                            <div class="col-md-7 mt-3">
                                <span>
                                    <i class="fa-solid fa-plate-wheat fa-lg"></i>
                                </span>
                                Шаг ${StepformIdx + 1}
                                <input type="hidden" name="steps-${StepformIdx}-step" id="id_steps-${StepformIdx}-step" value=${StepformIdx + 1}>

                                <textarea name="steps-${StepformIdx}-how_to_cook" cols="40" rows="10" class="form-control mt-3" placeholder="Введите инструкцию..." 
                                id="id_steps-${StepformIdx}-how_to_cook"></textarea>
                            </div>
                            <div class="col-md-5 mt-5">
                                <label for="id_steps-${StepformIdx}-image">
                                    <img class="img-thumbnail custom-file-upload" id="ingredient-preview-${StepformIdx}" width="100%" height="264px" src="/static/img/recipes/ingredient.png" alt="Image preview">
                                </label>
                                <input type="file" name="steps-${StepformIdx}-image" class="form-control" placeholder="Выберите файл" accept="image/*" id="id_steps-${StepformIdx}-image" style="display: none;">
                            </div>
                        </div>
                        <div class="col">
                            <button type="button" class="remove-step-btn btn btn-danger mt-3 w-100">
                                Удалить шаг
                            </button>
                        </div>
        `;

    stepFormsetContainer.appendChild(stepsFormsetItem);
}
addStepButton.addEventListener('click', (e) => {
    const StepformIdx = parseInt(stepsTotalForms.value);
    createStepForm(StepformIdx);
    stepsTotalForms.value = StepformIdx + 1;

    const imageInput = document.getElementById(`id_steps-${StepformIdx}-image`);
    const imagePreview = document.getElementById(`ingredient-preview-${StepformIdx}`);
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});

stepFormsetContainer.addEventListener('click', (e) => {
    const StepformIdx = parseInt(stepsTotalForms.value);
    if (e.target.classList.contains('remove-step-btn')) {
        const formset = e.target.closest('.step-formset-item');
        formset.remove();
        stepsTotalForms.value = StepformIdx - 1;
    }
});



