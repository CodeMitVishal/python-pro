"""Module 29 · Trees and binary search trees

A TREE is nodes with children and no cycles: folders, HTML (the DOM), org charts, JSON.
A BINARY SEARCH TREE (BST) keeps smaller values left and bigger values right, so
search/insert take O(log n) when the tree is balanced.

Traversals (the order you visit nodes):
  pre-order  (node, left, right)   copy a tree, print folder structures
  in-order   (left, node, right)   a BST comes out SORTED
  post-order (left, right, node)   delete/size: children before the parent
  level-order (row by row)         uses a queue (breadth-first)

Run it:  python 29_algorithms/03_trees.py
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    value: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def insert(root: TreeNode | None, value: int) -> TreeNode:
    if root is None:
        return TreeNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root


def contains(root: TreeNode | None, value: int) -> bool:
    while root:                                       # iterative: no recursion limit
        if value == root.value:
            return True
        root = root.left if value < root.value else root.right
    return False


def in_order(node: TreeNode | None) -> list[int]:
    return in_order(node.left) + [node.value] + in_order(node.right) if node else []


def pre_order(node: TreeNode | None) -> list[int]:
    return [node.value] + pre_order(node.left) + pre_order(node.right) if node else []


def height(node: TreeNode | None) -> int:
    return 1 + max(height(node.left), height(node.right)) if node else 0


def level_order(root: TreeNode | None) -> list[list[int]]:
    levels, queue = [], deque([root] if root else [])
    while queue:
        levels.append([n.value for n in queue])
        for _ in range(len(queue)):
            n = queue.popleft()
            queue.extend(c for c in (n.left, n.right) if c)
    return levels


root = None
for v in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, v)

print("in-order (sorted!):", in_order(root))
print("pre-order:         ", pre_order(root))
print("level by level:    ", level_order(root))
print("height:", height(root), "| contains 60:", contains(root, 60), "| contains 65:", contains(root, 65))

# The danger: inserting SORTED data makes a "tree" that's really a linked list
skewed = None
for v in range(1, 8):
    skewed = insert(skewed, v)
print("height after sorted inserts:", height(skewed), "<- O(n), not O(log n)")
# Real systems use self-balancing trees (red-black, B-trees in databases) to avoid this.
