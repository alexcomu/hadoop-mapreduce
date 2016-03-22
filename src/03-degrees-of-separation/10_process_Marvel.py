__author__ = 'alexcomu'
# Call this script passing the ID of the character you would like to start.
# Refer to 09_Marvel-names.txt

# How to run:
# python 10_process_Marvel.py HEROEID

import sys

print '### Creating BFS from user: ' + sys.argv[1]

with open("src/03-degrees-of-separation/BFS-iteration-0.txt", "w") as outFile:
    # output File

    with open("utils/09_Marvel-Graph.txt", "r") as f:
        # input File

        for line in f:
            # Parse the row
            fields = line.split()
            heroID = fields[0]
            numConnections = len(fields) - 1
            connections = fields[1:]

            color = 'WHITE'
            distance = 9999

            if heroID == sys.argv[1]:
                # This is my hero!
                color = 'GRAY'
                distance = 0

            if heroID != '':
                # Write into file!
                edges = ','.join(connections)
                outStr = '|'.join((heroID, edges, str(distance), color))
                outFile.write(outStr)
                outFile.write("\n")
        f.close()

outFile.close()


