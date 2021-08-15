function vegan_selected(guest_id) {
	var e = document.getElementById("menu_"+guest_id);
	if (e != null) {
		if (document.getElementById("vegan_"+guest_id).checked == true) {
			e.style.display = "none";
		} else {
			e.style.display = "block";
		}
	}
}

function attendance_changed(value, guest_id) {
	var display = "none";
	if (value == "day") {
		display = "block";
	}

	var e = document.getElementById("choices_" + guest_id);
	if (e != null) {
		e.style.display = display;
	}
}
