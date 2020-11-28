function loadSpectralFeatures(url) {
	if (location.href.includes('?')) {
		    history.pushState({}, null, location.href.split('?')[0]);
		    location.reload();
	}
  //window.location.href = url
}

function loadRhythmicFeatures(url) {
	if (location.href.includes('?')) {
		    history.pushState({}, null, location.href.split('?')[0]);
	}
	url= location.href+'?feature_type=rhythmic';
	location.href = url;
}

function loadDeltaFeatures(url) {
	if (location.href.includes('?')) {
		    history.pushState({}, null, location.href.split('?')[0]);
	}
	url= location.href+'?feature_type=deltas';
	location.href = url;

}

