$(function() {
    function loadFilaments() {
        $.get("/plugin/printmanager/get_filaments", function(data) {
            let filamentList = $("#filament_list");
            filamentList.empty();
            data.forEach(function(filament) {
                filamentList.append(`<div style="border: 1px solid #000; padding: 10px; margin: 10px;">
                    <div style="background-color: ${filament.color}; width: 20px; height: 20px; border-radius: 50%;"></div>
                    <span>${filament.name}</span>
                    <div>
                        <div style="width: ${filament.usage / 10}%; background-color: #00f; height: 10px;"></div>
                    </div>
                </div>`);
            });
        });
    }

    function loadPrints() {
        $.get("/plugin/printmanager/get_prints", function(data) {
            let printHistory = $("#print_history");
            printHistory.empty();
            data.forEach(function(print) {
                printHistory.append(`<div>
                    <span>${print.name}</span> - 
                    <span>${print.filament_color}</span> - 
                    <span>${print.filament_amount}g</span>
                </div>`);
            });
        });
    }

    $("#add_print_form").submit(function(event) {
        event.preventDefault();
        let printData = {
            name: $("#print_name").val(),
            filament_color: $("#filament_color").val(),
            filament_amount: $("#filament_amount").val()
        };
        $.post("/plugin/printmanager/add_print", JSON.stringify(printData), function(response) {
            if (response.success) {
                loadPrints();
            }
        });
    });

    loadFilaments();
    loadPrints();
});
