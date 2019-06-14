

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("contentContainer");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  /*tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }*/

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  /*evt.currentTarget.className += " active";*/
}

openTab(null, 'videosTab');

function loadStuff(List, container) {
  var row = document.createElement("div");
  row.className = "row";
  document.getElementById(container).appendChild(row);
  for (i = 0; i < 3; i++) {
    var column = document.createElement("div");
    column.className = "column";
    row.appendChild(column);
  }
  for (i = 0; i < List.length; i++) {
    addElement(container, i%3, List[i]);
  }
}

function addElement(container, columnIndex, url) {
  var media;
  if(container == "imagesTab") {
    media = document.createElement('img');
    media.src = url;
    media.addEventListener("click", function() {
        var url_to = './frame.php';
        var form = $('<form action="' + url_to + '" method="post">' +
          '<input type="text" name="frame" value=\"' + url + '\" />' +
          'type="hidden" </form>');
        $('body').append(form);
        form.submit();
    }, false);
  } else {
    media = document.createElement('video');
    media.controls = true;
    src = document.createElement('source');
    src.src = url;
    src.type = "video/mp4";
    media.appendChild(src);
  }
  columns = document.querySelectorAll("#" + container + " .column");
  columns[columnIndex].appendChild(media);
}
