
$(document).ready(function() {
	$(".chatIcon div").click(function(e) {
		$(".chatbox-holder").height("50px");
        $(".chatIcon").addClass("hidden");
		$(".close").click(function() {
                    $(".chatbox-holder").addClass("hidden")
                    $(".boxed").height("50px");
                    $("#dvEbixChat").html("")
                });
		var _height = $(".chatbox-holder").height();
		  $(".chatbox").animate({ height: "540px" },"slow");
		if (_height == "50") {
			$(".chatbox-holder").removeClass("hidden")
			$(".chatbox-holder").height("540px");
			$("#chatbox").html("")
			$("#dots").removeClass("hidden");
            setTimeout(
				function() {
					var botHtml = $("#msg1").html();
					$("#dvEbixChat").append(botHtml);
					$("#dots").addClass("hidden");
				}, 200);
			$("#dots").removeClass("hidden");
			setTimeout( function() {
			onLoad();
			},1000)

		} else {
			$(".chatbox-holder").addClass("hidden")
			$(".chatbox-holder").height("44px");
		}

	});
});
function onLoad() {
	var botHtml = $("#dvOptions").html()
	$("#dvEbixChat").append(botHtml);
	$("#dots").addClass("hidden");
	$("#dvEbixChat").animate({
		scrollTop: $('#dvEbixChat').prop("scrollHeight")
	}, 1000)
	$("#dvEbixChat").animate({
		scrollTop: $('#dvEbixChat').prop("scrollHeight")
	}, 1000)
}
function getBotResponse(obj) {
    var _id = $(obj).attr("id");
    var _value = $(obj).text();
    var rawText=""
    var userHtml=""
    if(_value == "Approve")
       rawText = _value + "_" + _id
    else
    {
         rawText = $("#textInput").val();
         userHtml = '<div class="message-user">User</div><div class="message-box-holder"><div class="message-box"><span>' + rawText + "</span></div></div>";
         $("#dvEbixChat").append(userHtml);
	 }
	$("#textInput").val("");
	ScrollBottom();
	$("#dots").removeClass("hidden");
    $('#btnVoice').removeClass("voiceGreen")
	if(rawText.indexOf("main menu")>0)
	{
	    onLoad();
	    $('#btnVoice').click()
	    return true;
	  }
	$.get("/get", {
		msg: rawText
	}).done(function(data) {
		var botHtml = data;
		$("#dvEbixChat").append(botHtml);
		$("#dots").addClass("hidden");
		if(data.indexOf("Bye.") > 0)
    		  $('#btnVoice').removeClass("voiceGreen")
        else if($("#btnVoice").hasClass("voiceGreen"))
              $('#btnVoice').click()
       if($("#btnVoice").hasClass("voiceGreen"))
            $("#dots").removeClass("hidden");
       ScrollBottom();
	});
}

function ScrollBottom(){
    $("#dvEbixChat").animate({
                scrollTop: $('#dvEbixChat').prop("scrollHeight")
            }, 1000);
}

function VoiceCommand(voice_msg){
    rawText = voice_msg
    $("#dots").removeClass("hidden");
    $('#btnVoice').addClass("voiceGreen")
    ScrollBottom();
 	$.get("/speech", {
		msg: rawText
	}).done(function(data) {
		var botHtml = data;
		$("#dots").removeClass("hidden");
		$("#textInput").val(botHtml);
		getBotResponse($("#textInput"))
		ScrollBottom();
	});
}

function approveTickets(obj){
getBotResponse(obj);
}
function GetApprove()
{
   $("#dvEbixChat").append("<div>Ticket Approved</div>")
}
function Close()
    {
    $(".chatbox").animate({ height: "20px" },"slow");
       $("#dvEbixChat").html("")
       $("#dots").addClass("hidden");
       $('#btnVoice').removeClass("voiceGreen");
       $(".chatIcon").removeClass("hidden");
     }
$("#textInput").keypress(function(e) {
	if (e.which == 13) {
		getBotResponse();
	}
});
function action(obj) {
	val = $(obj).text();
	$(obj).addClass("optionClick");
	$("#textInput").val(val)
	getBotResponse(obj);
}
