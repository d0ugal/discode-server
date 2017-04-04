import jinja2

_COMMENT_ROW = jinja2.Template("""
<tr id="C{{ lineno }}">
  <td colspan="2" class="comments">
    {% for comment in comments %}
    <div class="comment">
      <p>{{ comment }}</p>
    </div>
    {% endfor %}
  </td>
</tr>
""")


def comment_row(lineno, comments):
    return _COMMENT_ROW.render(lineno=lineno, comments=comments)
