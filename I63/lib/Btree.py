# Code source modifié de : https://www.askpython.com/python/examples/balanced-binary-tree1

class BinaryTreeNode:
    
  def __init__(self, data):
    self.val = data
    self.leftChild = None
    self.rightChild = None
     
    def insert(root,newValue):
        #if binary search tree is empty, make a new node and declare it as root

        if root is None:
            root=BinaryTreeNode(newValue)
            return root
        #binary search tree is not empty, so we will insert it into the tree
        #if newValue is less than value of data in root, add it to left subtree and proceed recursively
        if newValue<root.data:
            root.leftChild=insert(root.leftChild,newValue)
        else:
            #if newValue is greater than value of data in root, add it to right subtree and proceed recursively
            root.rightChild=insert(root.rightChild,newValue)

        return root
