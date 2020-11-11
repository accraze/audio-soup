function toggleMetadataForm(e, sampleId) {
	$(e).attr('disabled', true)
  document.getElementById("modal-card2_"+sampleId+"-metadata-form").style.visibility = 'visible';
  document.getElementById("modal-card2_"+sampleId+"-metadata").style.visibility = 'hidden';
}

function cancelMetadataForm(sampleId) {
  document.getElementById("modal-card2_"+sampleId+"-edit-btn").disabled = false;
  document.getElementById("modal-card2_"+sampleId+"-metadata-form").style.visibility = 'hidden';
  document.getElementById("modal-card2_"+sampleId+"-metadata").style.visibility = 'visible';
}
