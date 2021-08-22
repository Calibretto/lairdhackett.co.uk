function claim(gift_id) {
	var e = document.getElementById('claim_name_'+gift_id);
	if (e != null) {
		var name = e.value;
		if (name.length > 0) {
			e = document.getElementById('gift_form_'+gift_id);
			if (e != null) {
				e.submit();
			} else {
				alert("Unable to claim gift - this should not happen - please try again.");
			}
		} else {
			alert("Please enter your full name to claim this gift.");
		}
	} else {
		alert("Unable to claim gift - this shouldn't happen - please try again.");
	}
}
