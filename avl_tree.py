class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # a new node is a leaf


class AVLTree:
    def __init__(self):
        self.root = None

    # ---------- helpers ----------
    def height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    # ---------- rotations ----------
    def rotate_right(self, y):
        #       y                x
        #      / \              / \
        #     x   C    -->     A   y
        #    / \                  / \
        #   A   B                B   C
        x = y.left
        y.left = x.right
        x.right = y
        self.update_height(y)  # y is now lower, update it first
        self.update_height(x)
        return x

    def rotate_left(self, x):
        #     x                    y
        #    / \                  / \
        #   A   y      -->       x   C
        #      / \              / \
        #     B   C            A   B
        y = x.right
        x.right = y.left
        y.left = x
        self.update_height(x)
        self.update_height(y)
        return y

    # ---------- insertion ----------
    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # 1. Normal BST insertion
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # duplicates are ignored

        # 2. Update height of this ancestor
        self.update_height(node)

        # 3. Check balance factor
        balance = self.balance_factor(node)

        # 4. Fix imbalance (four cases)
        if balance > 1 and key < node.left.key:       # Left-Left
            return self.rotate_right(node)

        if balance > 1 and key > node.left.key:       # Left-Right
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and key > node.right.key:     # Right-Right
            return self.rotate_left(node)

        if balance < -1 and key < node.right.key:     # Right-Left
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node  # already balanced

    # ---------- utilities ----------
    def inorder(self, node="start"):
        if node == "start":
            node = self.root
        if node is None:
            return []
        return self.inorder(node.left) + [node.key] + self.inorder(node.right)

    def is_balanced(self, node="start"):
        if node == "start":
            node = self.root
        if node is None:
            return True
        return (abs(self.balance_factor(node)) <= 1
                and self.is_balanced(node.left)
                and self.is_balanced(node.right))

    def display(self, node="start", prefix="", is_left=True):
        if node == "start":
            node = self.root
        if node is None:
            return
        self.display(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + f"{node.key} (bf={self.balance_factor(node)})")
        self.display(node.left, prefix + ("    " if is_left else "│   "), True)


if __name__ == "__main__":
    tree = AVLTree()

    # Sorted input would make a plain BST a linked list; AVL keeps it balanced
    for k in [10, 20, 30, 40, 50, 25]:
        tree.insert(k)
        print(f"\nInserted {k}:")
        tree.display()

    print("\nIn-order:", tree.inorder())
    print("Balanced:", tree.is_balanced())
    print("Root:", tree.root.key, "| Height:", tree.root.height)