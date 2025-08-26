document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.querySelector(".form-row-add-service-btn");
    const container = document.querySelector(".form-service-rows");
    const totalForms = document.querySelector("#id_service_settings-TOTAL_FORMS");
    const emptyFormTemplate = document.querySelector("#empty-form");

    const addBtnUnit = document.querySelector(".form-row-add-serviceunit-btn");
    const containerUnit = document.querySelector(".form-serviceunit-rows");
    const totalFormsUnit = document.querySelector("#id_units_measurement-TOTAL_FORMS");
    const emptyFormTemplateUnit = document.querySelector("#empty_form_serviceunit");

    addBtn.addEventListener("click", function () {
        const formIndex = parseInt(totalForms.value);

        const newForm = emptyFormTemplate.firstElementChild.cloneNode(true);

        const elements = newForm.querySelectorAll('input, select, textarea, label');
        elements.forEach(element => {
            if (element.name) {
                element.name = element.name.replace('__prefix__', formIndex);
            }
            if (element.id) {
                element.id = element.id.replace('__prefix__', formIndex);
            }
            if (element.htmlFor) {
                element.htmlFor = element.htmlFor.replace('__prefix__', formIndex);
            }
        });
        newForm.id = `form-service-${formIndex}`;
        container.appendChild(newForm);
        totalForms.value = formIndex + 1;
    });

    container.addEventListener("click", function (event) {
        const removeBtn = event.target.closest(".form-row-remove-btn");
        if (!removeBtn) return;

        const formRow = removeBtn.closest(".form-service");
        if (!formRow) return;

        const deleteInput = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');

        if (deleteInput) {
            deleteInput.checked = true;
            formRow.style.display = "none";
        } else {
            formRow.remove();

            totalForms.value = parseInt(totalForms.value) - 1;
        }
    });

    addBtnUnit.addEventListener("click", function () {
        const formIndex = parseInt(totalFormsUnit.value);

        const newForm = emptyFormTemplateUnit.firstElementChild.cloneNode(true);

        const elementsUnit = newForm.querySelectorAll('input, select, textarea, label');
        elementsUnit.forEach(el => {
            if (el.name) el.name = el.name.replace('__prefix__', formIndex);
            if (el.id) el.id = el.id.replace('__prefix__', formIndex);
            if (el.htmlFor) el.htmlFor = el.htmlFor.replace('__prefix__', formIndex);
        });

        newForm.id = `form-serviceunit-${formIndex}`;
        containerUnit.appendChild(newForm);

        totalFormsUnit.value = formIndex + 1;
    });

    containerUnit.addEventListener("click", function (event) {
        const removeBtn = event.target.closest(".form-row-remove-btn");
        if (!removeBtn) return;

        const formRow = removeBtn.closest(".form-serviceunit");
        if (!formRow) return;

        const deleteInput = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');

        if (deleteInput) {
            deleteInput.checked = true;
            formRow.style.display = "none";
        } else {
            formRow.remove();
            totalFormsUnit.value = parseInt(totalFormsUnit.value) - 1;
        }
    });

});
