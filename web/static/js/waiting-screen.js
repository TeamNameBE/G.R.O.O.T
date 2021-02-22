var interval = setInterval(get_results, 500);

function get_results(){
    $.get(
        "api/result?job=" + job_id,
        function(data) {
            if(data["status"] == "running"){
                $("#position").text = data["position"];
                $("#total_jobs").text = data["running_jobs"];
            } else if(data['status'] == "done") {
                $("#result_div").html("<h3>" + data["result"] + "</h3>");
                $("#title").text("Votre résultat est disponible !");
                $("#queue_position").css("display", "none");
                clearInterval(interval);
            } else if(data["status"] == "error"){
                $("#title").text("Une erreur est survenue !");
                $("#queue_position").css("display", "none");
                $("#result").text(data["error"]);
            }
        }
    );
}