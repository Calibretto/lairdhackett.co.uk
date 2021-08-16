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
	var opposite = "block";
	if (value == "day") {
		display = "block";
		opposite = "none";
	}

	var e = document.getElementById("choices_" + guest_id);
	if (e != null) {
		e.style.display = display;
	}

	e = document.getElementById("evening_only_" + guest_id);
	if (e != null) {
		e.style.display = opposite;
	}

}
