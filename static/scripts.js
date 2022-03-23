$(document).ready(function () {
	setInterval(function () {
		$("#sensor-dashboard").load(location.href + " #sensor-dashboard");
	}, 30000);
});
