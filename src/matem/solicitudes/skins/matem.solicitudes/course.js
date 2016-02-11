CourseFieldFunctions = new Object()

CourseFieldFunctions.getRows = function(tbody) {
  /* Return <tr> rows of <table> element */

  var rows = new Array()

  child = tbody.firstChild;
  while(child != null) {
    if(child.tagName != null) {
      if(child.tagName.toLowerCase() == "tr") {
        rows = rows.concat(child);
      }
    }
    child = child.nextSibling;
  }

  return rows;
}

CourseFieldFunctions.addRow = function(id) {
  /* Explitcly add row for given DataGridField

    @param id Archetypes field id for the widget
  */
  // fetch required data structure
    var tbody = document.getElementById("coursewidget-tbody-" + id);
    var rows = this.getRows(tbody);
    var lastRow = rows[rows.length-1];

    console.log(lastRow)

    var oldRows = rows.length;

    // Create a new row
    var newtr = this.createNewRow(lastRow);
    
    // Put new row to DOM tree before template row
    newNode = lastRow.parentNode.insertBefore(newtr, lastRow);

  // update orderindex hidden fields
  //this.updateOrderIndex(tbody);

}

CourseFieldFunctions.createNewRow = function(tr) {
  /* Creates a new row

     @param tr A row in a table where we'll be adding the new row
  */

    var tbody = this.getParentElementById(tr, "coursewidget-tbody");
    var rows = this.getRows(tbody);

    // hidden template row
    var lastRow = rows[rows.length-1];

    var newtr = document.createElement("tr");
    newtr.setAttribute("id", "coursewidget-row");
    newtr.setAttribute("class", "coursewidget-row");

  // clone template contents from the last row to the newly created row
  // HOX HOX HOX
  // If f****ng IE clones lastRow directly it doesn't work.
  // lastRow is in hidden state and no matter what you do it remains hidden.
  // i.e. overriding class doesn't bring it visible.
  // In Firefox everything worked like a charm.
  // So the code below is really a hack to satisfy Microsoft codeborgs.
  // keywords: IE javascript clone clonenode hidden element render visibility visual
    child = lastRow.firstChild;
    while(child != null) {
      newchild = child.cloneNode(true);
      newtr.appendChild(newchild);
      child = child.nextSibling;
    }

    return newtr;
}

CourseFieldFunctions.getParentElementById = function(currnode, id) {
    /* Find the first parent node with the given id

      Id is partially matched: the beginning of
      an element id matches parameter id string.

      Currnode: Node where ascending in DOM tree beings
      Id: Id string to look for.

    */

    id = id.toLowerCase();
    var parent = currnode.parentNode;

    while(true) {

      var parentId = parent.getAttribute("id");
      if(parentId != null) {
         if(parentId.toLowerCase().substring(0, id.length) == id) break;
      }

        parent = parent.parentNode;
        // Next line is a safety belt
        if(parent.tagName.toUpperCase() == "BODY")
            return null;
    }

    return parent;
}




