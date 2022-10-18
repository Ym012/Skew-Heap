from binarytree import Node, NodeTypeError
from numpy import random

class SkewHeap:
    """Represents a skew heap.
        :param root: root of the heap (default: None).
        :type Node: binarytree.Node
        :param visualizeSteps: set to True, to draw the heap after relevant steps; False, otherwise
        :type visualizeSteps: bool
        :param flipProbability: The probability that we flip left/right children at some node
        :type flipProbability: float
    """
    def __init__(self, root = None, visualizeSteps = False, flipProbability = 1):
        if root is not None and not isinstance(root, Node):
            raise NodeTypeError('root must be a Node instance')
        self.root = root
        self.visualizeSteps: bool = visualizeSteps
        self.flipProbability = flipProbability
        self.comparisonsOperationsCount = 0
        self.flipOperationsCount = 0

    def find_min(self):
        """Return the node with the smallest key in the heap. (which is the root)
            :return: root
            :rtype: binarytree.Node
        """
        return self.root

    def insert(self, node):
        """insert a new node into the heap
            :param node: node to insert
            :type node: Node
        """
        if (self.visualizeSteps):
            print("insert {}".format(node.value))
        singletonHeap = SkewHeap(node)
        self.meld(singletonHeap)

    def meld(self, other):
        """melds the current heap with the other heap
            :param other: another skew heap
            :type other: SkewHeap
        """
        if (self.visualizeSteps):
            print("Melding {} and {}".format(self, other))

        lastMergedNode: Node = None
        currentNodeH1 :Node = self.root
        currentNodeH2 :Node = other.root

        while (currentNodeH1 is not None or currentNodeH2 is not None):
            self.comparisonsOperationsCount += 1
            if (currentNodeH2 is None or (currentNodeH1 is not None and currentNodeH1.value <= currentNodeH2.value)):
                smallestNode: Node = currentNodeH1
                currentNodeH1 = currentNodeH1.right
            else:
                smallestNode: Node = currentNodeH2
                currentNodeH2 = currentNodeH2.right

            smallestNode.parent = lastMergedNode
            if (lastMergedNode is None):  # Then we are at the root
                self.root = smallestNode
            else:
                lastMergedNode.right = smallestNode
            lastMergedNode = smallestNode

        if (self.visualizeSteps):
            print("After merging the right spines: {}".format(self))

        self.flipAfterMeld(lastMergedNode)

    def flipAfterMeld(self, bottomMostNode):
        """goes upwards in the heap and flip left/right children
            :param bottomMostNode: node whose ancestors will have their left/right children swapped
            :type bottomMostNode: Node
        """
        while (bottomMostNode.parent is not None):
            bottomMostNode = bottomMostNode.parent

            binomialRandom = random.binomial(1, self.flipProbability)
            if (binomialRandom == 0):
                continue

            self.flipOperationsCount += 1
            temp = bottomMostNode.left
            bottomMostNode.left = bottomMostNode.right
            bottomMostNode.right = temp
            if (self.visualizeSteps):
                print("After swapping children of node {parent}:".format(parent = bottomMostNode.value))
                print(self)

    def extract_min(self):
        """extracts the minimum node from the heap"""
        if (self.isEmpty()):
            return None

        result = self.root
        if (self.visualizeSteps):
            print("extract min: returns {}".format(result.value))
        rightSubHeap = SkewHeap(self.root.right) # craete a heap with the right sub-tree of the root
        self.root = self.root.left # by that we delete the root and set the heap to be its left sub-tree
        result.left = None
        result.right = None
        if (self.root is None and rightSubHeap.isEmpty()):
            return result
        self.meld(rightSubHeap)
        return result

    def isEmpty(self):
        """
            :return: True if the heap is empty, False otherwise
            :rtype: bool
        """
        return self.root is None

    def decrease_key (self, node, newKey):
        """decrease the key of a given node
            :param node: the node, for which we want to decrease the key
            :type node: Node
            :param newKey: new key value (must be a number).
            :type newKey: int | float | numbers.Number
        """
        if (self.visualizeSteps):
            print("decrease key of node {} to {}".format(node.value, newKey))
        parent: Node = node.parent
        # cut out node and its subtree:
        if (parent.right == node):
            parent.right = None
        elif (parent.left == node):
            parent.left = None
        node.parent = None
        if (self.visualizeSteps):
            print("cut out the node and its subtree")

        # update key of the node
        node.value = newKey
        # meld x and subtree with the rest of the heap
        newHeap = SkewHeap(node)
        self.meld(newHeap)

    def setVisualizeSteps(self, visualizeSteps):
        """setting visualizeSteps will result in drawing the heap after relevant steps
            :param visualizeSteps: set to True, to draw the heap after relevant steps; False, otherwise
            :type visualizeSteps: bool
        """
        self.visualizeSteps = visualizeSteps

    def __str__(self):
        """Return the pretty-print string for the heap.
            :return: Pretty-print string.
            :rtype: str | unicode
        """
        return self.root.__str__()