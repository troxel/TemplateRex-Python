{'admin': 'Admin',
 'cell_complex': '<td>Battery $cell_id:$cell_volt</td>',
 'ftr': 'Ftr',
 'main': '<!DOCTYPE html>\n'
         '\n'
         'Top main\n'
         '\n'
         '$tbl\n'
         '\n'
         '$tbl_complex\n'
         '\n'
         '\n'
         '<ul>\n'
         '$user_sec\n'
         '</ul>\n'
         '\n'
         '\n'
         '$admin\n'
         '\n'
         '$ftr\n'
         'Bottom main\n',
 'row': '<tr><td>Name: $name</td><td>Color: $color</td></tr>',
 'row_complex': '<tr>\n    $cell_complex\n    </tr>',
 'tbl': '<table>\n  <caption>List of $category </caption>\n  $row\n</table>',
 'tbl_complex': '<table>\n'
                '  <caption>Battery Voltages</caption>\n'
                '  $row_complex\n'
                '</table>',
 'user_sec': '<li> user.username'}
