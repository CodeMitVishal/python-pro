"""Module 29 · Stacks, queues and linked lists

STACK  -> Last In, First Out (LIFO): undo history, the call stack, matching brackets
QUEUE  -> First In, First Out (FIFO): print jobs, task queues, breadth-first search
LINKED LIST -> nodes pointing to the next node: O(1) insert at the front, no random access

Run it:  python 29_algorithms/02_stacks_queues_linked_lists.py
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


# --- 1. Stack with a list: push = append, pop = pop (both O(1) at the end) ----------------------
def is_balanced(text: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)                      # push an opener
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:   # pop must match
                return False
    return not stack                              # everything opened was closed


for expr in ["(a[1] + b) * {c}", "(]", "((x)"]:
    print(f"{expr!r:<20} balanced: {is_balanced(expr)}")

undo: list[str] = []
for action in ["type 'Hi'", "bold", "type '!'"]:
    undo.append(action)
print("undo:", undo.pop(), "| then:", undo.pop())   # last action first

# --- 2. Queue with deque: append + popleft are O(1) (list.pop(0) is O(n)!) ---------------------------
printer = deque(["report.pdf", "invoice.pdf"])
printer.append("photo.png")                       # joins at the back
while printer:
    print("printing", printer.popleft())          # served from the front


# --- 3. A linked list, built by hand ---------------------------------------------------------------------
@dataclass
class Node:
    value: int
    next: Node | None = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None

    def push_front(self, value: int) -> None:      # O(1): no shifting, unlike list.insert(0, x)
        self.head = Node(value, self.head)

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next

    def reverse(self) -> None:                    # the classic interview question
        prev, node = None, self.head
        while node:
            node.next, prev, node = prev, node, node.next
        self.head = prev


ll = LinkedList()
for v in [3, 2, 1]:
    ll.push_front(v)
print("linked list:", list(ll))                    # [1, 2, 3]
ll.reverse()
print("reversed:   ", list(ll))                    # [3, 2, 1]

# In Python you'll rarely write a linked list: use list or deque.
# But "reverse a linked list" teaches pointer thinking used everywhere (trees, graphs).
