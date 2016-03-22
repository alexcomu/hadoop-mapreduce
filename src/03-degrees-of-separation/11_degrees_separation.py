__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class Node:
    # Abstraction of Character

    # Constructor
    def __init__(self):
        self.characterID = ''
        self.connections = []
        self.distance = 9999
        self.color = 'WHITE'

    # Format: HEROID|EDGES|DISTANCE|COLOR
    def fromLine(self, line):
        fields = line.split('|')
        if len(fields) == 4:
            self.characterID = fields[0]
            self.connections = fields[1].split(',')
            self.distance = int(fields[2])
            self.color = fields[3]

    # Return the line with the correct format
    def getLine(self):
        connections = ','.join(self.connections)
        return '|'.join((self.characterID, connections, str(self.distance), self.color))

class MRBFSIteration(MRJob):

    # set the input / output protocol to write and read the file
    # Json is probably the most used
    INPUT_PROTOCOL = RawValueProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    # Pass the parameter to everybody who needs it as input value
    # --target=12345
    def configure_options(self):
        super(MRBFSIteration, self).configure_options()
        self.add_passthrough_option('--target', help="Insert the ID of the character we are looking for")

    def mapper(self, _, line):
        node = Node()
        node.fromLine(line)
        # Look for grey nodes
        # At first iteration for ID = 100
        # 100|5432,3554,3116,4125,1721,6187,1347|0|GRAY
        if (node.color == 'GRAY'):
            for connection in node.connections:
                # Create a node for each connections
                vnode = Node()
                vnode.characterID = connection
                vnode.distance = int(node.distance) + 1
                vnode.color = 'GRAY'
                if (self.options.target == connection):
                    # Got it!
                    counterName = ("Target ID " + connection +
                        " was hit with distance " + str(vnode.distance))
                    self.increment_counter('Degrees of Separation',
                        counterName, 1)
                yield connection, vnode.getLine()

            # We've processed this node, so color it black
            node.color = 'BLACK'

        # Emit the input node so we don't lose it.
        yield node.characterID, node.getLine()

    def reducer(self, key, values):
        # Base settings
        edges = []
        distance = 9999
        color = 'WHITE'

        # Data is grouped by HeroID, so for each value
        for value in values:
            node = Node()
            node.fromLine(value)

            # Extends the new array of connections
            if (len(node.connections) > 0):
                edges.extend(node.connections)

            # Set the new distance value if less than MAX
            if (node.distance < distance):
                distance = node.distance

            # If the node was already Black -> be black again
            if ( node.color == 'BLACK' ):
                color = 'BLACK'

            # If is not black -> become gray, will be checked on next iteration
            if ( node.color == 'GRAY' and color == 'WHITE' ):
                color = 'GRAY'

        # Prepare the new output line
        node = Node()
        node.characterID = key
        node.distance = distance
        node.color = color
        node.connections = edges[:500] # just a memory control

        yield key, node.getLine()

if __name__ == '__main__':
    MRBFSIteration.run()
