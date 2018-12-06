# By Hanwei Wang in Royal HaskoningDHV
# 03-12-2018

Path = 'LNGC_breakwater.pat'
name = Path.split('.')[0]
print(name)
with open(Path, 'r') as padfile:
    file = padfile.read()
    lines = file.split('\n')
    # num_Coordinate and num_panel are in the 3rd(2) line
    # information is in the 4th(3) line

    num_coordinate = lines[2].split(' ')
    while '' in num_coordinate:
        num_coordinate.remove('')

    # get number of coor and panels
    num_points = num_coordinate[4]
    num_panels = num_coordinate[5]

    # model information
    info_model = lines[3].strip()
    print(info_model)

    # get the coordinate of vertex
    block_length = 3
    list_points = (lines[ 3+2 : 3*int(num_points)+3: 3])

    # connectivity over each panel
    list_connectivity = (lines[ 3*int(num_points)+ 6  : 3*(int(num_points)+ int(num_panels)) + 6: 3])

    padfile.close()

"""
Write VTK file
"""

vtk_file = name+'.vtk'
with open(vtk_file, 'w') as outfile:
    # header
    outfile.write('# vtk DataFile Version 2.0\n')
    outfile.write('An case related object\n')
    outfile.write('ASCII\n')
    outfile.write('\n')
    outfile.write('DATASET UNSTRUCTURED_GRID\n')
    outfile.write('POINTS' +' '+ num_points +' '+ 'float\n')

    # vertex
    for vertex in list_points:
        outfile.write(vertex + '\n')
    outfile.write('\n')

    # Cells
    outfile.write('CELLS' + ' ' + num_panels + ' ' + str(5*int(num_panels)) + '\n')
    node_per_cell = []
    for cell in list_connectivity:
        # in .vtk the cell node start with 0, but 1 in .pat
        int_cell = list(map(lambda x:x-1,(list(map(int, cell.split())))))
        str_cell = list(map(str, int_cell))
        outfile.write(str(len(str_cell)) + ' ' + ' '.join(str_cell) + '\n')
        node_per_cell.append(len(str_cell))
    outfile.write('\n')

    # write the cell_type
    """
    General cases
    1d point cell(panel) --> 1
    2d panel cell 2(line) --> 3
                  3(triangle) --> 5
                  4(retangular) --> 9  ???
                  4 pixel(square) --> 8  ???
                  n vtk_polygon --> 7
    """

    outfile.write('CELL_TYPES'+' '+ num_panels+ '\n')

    # from node_per_cell --> type_per_cell

    def nodes2type(node):
        if node == 1:
            return 1
        elif node == 2:
            return 3
        elif node == 3:
            return 5
        elif node == 4:
            return 9
        elif node > 4:
            return 7
        else:
            print('Nonlinear cell type, not match')

    cell_type = list((map(nodes2type, node_per_cell)))
    i = 0
    while i < int(num_panels):
        outfile.write(str(cell_type[i]) + '\n')
        i += 1
    outfile.close()
    print(i)







