function loadSpectralFeatures(url) {
	if (location.href.includes('?')) {
		    history.pushState({}, null, location.href.split('?')[0]);
		    location.reload();
	}
  //window.location.href = url
}

function loadRhythmicFeatures(url) {
	console.log('load rhythmic features!!!');
	url= location.href+'?feature_type=rhythmic';
	console.log(url);
	location.href = url;
}

function loadDeltaFeatures(url) {
	url= location.href+'?feature_type=deltas';
	location.href = url;

}

