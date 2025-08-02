let newIndex = 1000;

function addNewInput(afterIndex) {
  const container = document.getElementById("segments-container");
  const afterRow = document.getElementById(`segment-row-${afterIndex}`);

  const newDiv = document.createElement("div");
  newDiv.className = "segment-row";
  newDiv.id = `segment-row-${newIndex}`;
  newDiv.innerHTML = `
 <label>시간</label>
  <input type="text" name="start${newIndex}" value="" class="time-input" placeholder="0:00.00">
  <label>가사</label>
  <input type="text" name="text${newIndex}" value="" class="lyric-input">

  <button type="button" onclick="addNewInput(${newIndex})" class="btn-icon">
    <img src="/static/img/add.png" alt="추가">
  </button>
  <input type="hidden" name="delete${newIndex}" value="0">
  <button type="button" onclick="deleteInput('segment-row-${newIndex}')" class="btn-icon">
    <img src="/static/img/delete.png" alt="삭제">
  </button>
  `;
  container.insertBefore(newDiv, afterRow.nextSibling);
  newIndex++;
}

function deleteInput(rowId) {
  const row = document.getElementById(rowId);
  if (row) {
    row.remove();
  }
}

function updateSegmentCountBeforeSubmit() {
  const rows = document.querySelectorAll("#segments-container .segment-row");
  document.querySelector('input[name="segment_count"]').value = rows.length;
}
