{'content': 'Main Content\n$tbl',
 'ftr': 'Ftr',
 'main': '<!DOCTYPE html>\n'
         '\n'
         '<html lang="en">\n'
         '<head>\n'
         '  <meta charset="utf-8">\n'
         '\n'
         '  <title>$title</title>\n'
         '  <meta name="description" content="Description">\n'
         '\n'
         '  <link rel="stylesheet" href="$url_base_css">\n'
         '</head>\n'
         '\n'
         '<body>\n'
         '  \n'
         '  <div> $navigation </div>\n'
         '  <div>  $content </div>\n'
         '  \n'
         '  <script src="$url_base_js"></script>\n'
         '</body>\n'
         '</html>\n',
 'main_child': '<!-- BASE name=t-base.html -->\n\n$content\n\n$ftr\n',
 'row': '<tr><td>$inc</td><td>Name: $name</td><td>Color: $color</td></tr>',
 'tbl': '<table>\n  <caption>List of flowers</caption>\n  $row\n</table>'}
