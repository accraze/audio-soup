function toggleMetadataForm(e, sampleId) {
	$(e).attr('disabled', true)
  document.getElementById("modal-card2_"+sampleId+"-metadata-form").style.display = 'inline';
  document.getElementById("modal-card2_"+sampleId+"-metadata").style.display = 'none';
}

function cancelMetadataForm(sampleId) {
  document.getElementById("modal-card2_"+sampleId+"-edit-btn").disabled = false;
  document.getElementById("modal-card2_"+sampleId+"-metadata-form").style.display = 'none';
  document.getElementById("modal-card2_"+sampleId+"-metadata").style.display = 'inline';
}
