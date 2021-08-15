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
