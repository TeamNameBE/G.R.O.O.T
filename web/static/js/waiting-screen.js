var interval = setInterval(get_results, 500);

function get_results(){
    $.get(
        "api/result?job=" + job_id,
        function(data) {
            if(data["status"] == "running"){
                $("#position").text = data["position"];
                $("#total_jobs").text = data["running_jobs"];
            } else if(data['status'] == "done") {
                $("#result_div").html(
                    "<h3>Cette image appartient probablement a la famille des "
                    + data["result"]["family"]
                    + " (Confiance: " + data["result"]["confidence"]
                    + ")</h3><div id='tweet_btn'></div>"
                );
                $("#title").text("Votre résultat est disponible !");
                $("#queue_position").css("display", "none");
                $("#tweet_btn").html("<a class='btn btn-primary' href='/tweet?job=" + job_id + "'>Tweeter le résultat</a>")
                clearInterval(interval);
            } else if(data["status"] == "error"){
                $("#title").text("Une erreur est survenue !");
                $("#queue_position").css("display", "none");
                $("#result").text(data["error"]);
            }
        }
    );
}