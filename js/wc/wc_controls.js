$(document).ready(function() {
	$("#s_games_list").dblclick(function() {
		var e = document.getElementById("s_games_list");
		var strUser = e.options[e.selectedIndex].value;
		var postLine = "launch?r=" + strUser;
		$.post(postLine);
	});
});