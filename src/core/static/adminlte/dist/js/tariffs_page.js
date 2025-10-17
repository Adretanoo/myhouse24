document.addEventListener("DOMContentLoaded", function () {
    const totalFormsInput = document.getElementById("id_tariffs_card-TOTAL_FORMS"); // <-- твій id
    let formIndex = parseInt(totalFormsInput.value);
    const addButton = document.querySelector(".form-row-add-websitetariffs-btn");
    const container = document.getElementById("form-websitetariff-rows");
    const emptyFormTemplate = document.getElementById("empty-form").firstElementChild;

    function getNextDisplayNumber() {
        const rows = container.querySelectorAll('.form-websitetariff');
        let max = 0;
        rows.forEach(row => {
            if (row.style.display !== 'none') {
                const h4 = row.querySelector('h4');
                if (h4) {
                    const num = parseInt(h4.textContent.replace(/\D/g, ''), 10);
                    if (!isNaN(num) && num > max) max = num;
                }
            }
        });
        return max + 1;
    }

    addButton.addEventListener("click", function () {
        const displayNumber = getNextDisplayNumber();
        const newForm = emptyFormTemplate.cloneNode(true);

        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIndex)
                                             .replace(/__display__/g, displayNumber);

        container.appendChild(newForm);

        formIndex++;
        totalFormsInput.value = formIndex;
    });

    document.addEventListener("click", function (e) {
        const removeBtn = e.target.closest(".remove-service");
        if (!removeBtn) return;
        e.preventDefault();

        const row = removeBtn.closest(".form-websitetariff");
        if (!row) return;

        const deleteInput = row.querySelector('input[type=checkbox][name$="DELETE"]');
        if (deleteInput) {
            deleteInput.checked = true;
            row.style.display = "none";
        } else {
            row.remove();
            totalFormsInput.value = parseInt(totalFormsInput.value, 10) - 1;
        }
    });
});
