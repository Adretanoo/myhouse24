document.addEventListener("DOMContentLoaded", function () {
    // ====== ДОКУМЕНТИ ======
    const totalFormsInput = document.getElementById("id_about_page_documents-TOTAL_FORMS");
    const docsContainer = document.getElementById("form-websitedocument-rows");
    const addDocButton = document.querySelector(".form-row-add-websitedocument-btn");
    const emptyFormTemplate = document.getElementById("empty-form")?.firstElementChild;

    if (totalFormsInput && docsContainer && addDocButton && emptyFormTemplate) {
        let formIndex = parseInt(totalFormsInput.value, 10);

        function attachDeleteHandler(btn) {
            btn.addEventListener("click", function (e) {
                e.preventDefault();

                const formRow = btn.closest(".form-websitedocument");
                if (!formRow) return;

                const deleteCheckbox = formRow.querySelector('input[type="checkbox"][name$="-DELETE"]');

                if (deleteCheckbox) {
                    deleteCheckbox.checked = true;
                    formRow.style.display = "none";
                } else {
                    formRow.remove();
                    totalFormsInput.value = Math.max(0, parseInt(totalFormsInput.value, 10) - 1);
                }
            });
        }

        docsContainer.querySelectorAll(".delete-document-btn, .remove-document")
            .forEach(attachDeleteHandler);

        addDocButton.addEventListener("click", function (e) {
            e.preventDefault();

            const newForm = emptyFormTemplate.cloneNode(true);
            newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIndex);

            docsContainer.appendChild(newForm);
            totalFormsInput.value = ++formIndex;

            const newDeleteBtn = newForm.querySelector(".delete-document-btn, .remove-document");
            if (newDeleteBtn) attachDeleteHandler(newDeleteBtn);
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const galleryContainer = document.getElementById("about-gallery-forms");
    const totalGalleryForms = document.getElementById("id_about_page_gallery-TOTAL_FORMS");

    if (galleryContainer && totalGalleryForms) {
        galleryContainer.addEventListener("click", function (e) {
            const removeBtn = e.target.closest(".remove-gallery");
            if (!removeBtn) return;
            e.preventDefault();

            const formBlock = removeBtn.closest(".about_gallery");
            if (!formBlock) return;

            const deleteCheckbox = formBlock.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (deleteCheckbox) {
                deleteCheckbox.checked = true;
                formBlock.style.display = "none";
            } else {
                formBlock.remove();
                totalGalleryForms.value = parseInt(totalGalleryForms.value, 10) - 1;
            }
        });
    }

    const additionalContainer = document.getElementById("about-additional-gallery-forms");
    const totalAdditionalForms = document.getElementById("id_about_page_additional_gallery-TOTAL_FORMS");

    if (additionalContainer && totalAdditionalForms) {
        additionalContainer.addEventListener("click", function (e) {
            const removeBtn = e.target.closest(".remove-gallery-additional");
            if (!removeBtn) return;
            e.preventDefault();

            const formBlock = removeBtn.closest(".about_additional_gallery");
            if (!formBlock) return;

            const deleteCheckbox = formBlock.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (deleteCheckbox) {
                deleteCheckbox.checked = true;
                formBlock.style.display = "none";
            } else {
                formBlock.remove();
                totalAdditionalForms.value = parseInt(totalAdditionalForms.value, 10) - 1;
            }
        });
    }
});
