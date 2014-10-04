%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The open items are as follows:</p>
<table border="1">
%for row in rows:
  <tr>
  <td>{{row.id}}</td>
    <td>{{row.task}}</td>
    <td><a href="/edit/{{row.id}}"> Edit</a></td>
  </tr>
%end
</table>
<br>
<hr>
<a href="http://localhost:8080/new">Create a new item...</a>

