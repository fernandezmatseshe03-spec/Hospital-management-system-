document.addEventListener("DOMContentLoaded", () => {

    // Prevent selecting appointment dates in the past
    const dateInput = document.querySelector(
        'input[name="appointment_date"]'
    );

    if (dateInput) {

        const today =
            new Date().toISOString().split("T")[0];

        dateInput.min = today;
    }


    // Medical record form
    const recordForm =
        document.getElementById("recordForm");

    const patientId =
        document.getElementById("patientId");


    if (recordForm && patientId) {

        recordForm.addEventListener(
            "submit",
            function () {

                const id = patientId.value.trim();

                if (!id) {

                    alert(
                        "Please enter a patient ID."
                    );

                    return;
                }

                this.action =
                    `/staff/patient/${id}/record`;
            }
        );
    }


    // Automatically remove flash messages
    setTimeout(() => {

        document
            .querySelectorAll(".flash")
            .forEach((element) => {

                element.style.transition =
                    "opacity 0.4s";

                element.style.opacity = "0";

                setTimeout(() => {
                    element.remove();
                }, 500);

            });

    }, 4500);

});