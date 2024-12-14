import tkinter as tk
from tkinter import messagebox
import time

# Best Fit Memory Manager Class
class BestFitMemoryManager:
    def __init__(self, blocks):
        self.blocks = blocks
        self.free_space = blocks[:]  # Copy of block sizes to track free space
        self.allocations = [[] for _ in blocks]  # Track allocations in each block

    def allocate_memory(self, process_size):
        best_index = -1
        for i, space in enumerate(self.free_space):
            if space >= process_size:  # Check if block has enough free space
                if best_index == -1 or space < self.free_space[best_index]:
                    best_index = i
        if best_index != -1:
            self.free_space[best_index] -= process_size  # Reduce free space
            process_id = f"P{process_size}"  # Create a process ID
            self.allocations[best_index].append(process_id)  # Add process to block
            return best_index, process_id
        return -1, None  # No suitable block found

    def release_memory(self, process_id):
        for i, allocs in enumerate(self.allocations):
            if process_id in allocs:
                alloc_size = int(process_id[1:])  # Extract size from process ID
                self.free_space[i] += alloc_size  # Restore free space
                self.allocations[i].remove(process_id)  # Remove process from block
                return True
        return False  # Process not found

    def memory_status(self):
        return [
            f"Block {i + 1}: {self.blocks[i]} KB - Free: {self.free_space[i]} KB - {' | '.join(allocs) if allocs else 'Empty'}"
            for i, allocs in enumerate(self.allocations)
        ]

# Tkinter UI
def allocate():
    try:
        process_size = int(entry_process_size.get())
        block_index, process_id = manager.allocate_memory(process_size)
        if block_index != -1:
            animate_search_and_allocation(block_index, process_size, process_id)
        else:
            messagebox.showerror("Error", f"No suitable block for process of size {process_size} KB.")
        update_status()
    except ValueError:
        messagebox.showerror("Error", "Invalid input for Process Size.")

def animate_search_and_allocation(block_index, process_size, process_id):
    # Animate the search process
    for i, space in enumerate(manager.free_space):
        block_labels[i].config(bg="blue")  # Highlight block being checked
        root.update()
        time.sleep(0.5)  # Pause to simulate evaluation
        if i == block_index:  # Mark the chosen block
            block_labels[i].config(bg="yellow")
        else:
            block_labels[i].config(bg="white")
    
    # Final allocation animation
    time.sleep(0.5)
    block_labels[block_index].config(
        bg="green", text=f"Block {block_index + 1}\nFree: {manager.free_space[block_index]} KB\n{process_id}"
    )

def release():
    process_id = entry_process_id.get()
    if manager.release_memory(process_id):
        update_status()
        refresh_blocks()
    else:
        messagebox.showerror("Error", f"Process {process_id} not found.")

def refresh_blocks():
    # Update the visual representation of memory blocks
    for i, allocs in enumerate(manager.allocations):
        free_space = manager.free_space[i]
        if not allocs:
            block_labels[i].config(bg="white", text=f"Block {i + 1}\nFree: {free_space} KB")
        else:
            block_labels[i].config(bg="green", text=f"Block {i + 1}\nFree: {free_space} KB\n{' | '.join(allocs)}")

def update_status():
    # Update memory status display
    memory_status.set("\n".join(manager.memory_status()))

# Initial Setup
blocks = [80, 250, 325, 550, 1000, 150]
manager = BestFitMemoryManager(blocks)

root = tk.Tk()
root.title("Best Fit Memory Allocation with Animated Search")

# Input Fields and Buttons
tk.Label(root, text="Enter Process Size (KB):").pack(pady=5)
entry_process_size = tk.Entry(root)
entry_process_size.pack(pady=5)
tk.Button(root, text="Allocate", command=allocate).pack(pady=5)

tk.Label(root, text="Enter Process ID to Release:").pack(pady=5)
entry_process_id = tk.Entry(root)
entry_process_id.pack(pady=5)
tk.Button(root, text="Release", command=release).pack(pady=5)

# Visual Representation of Memory Blocks
block_labels = []
for i, block_size in enumerate(blocks):
    label = tk.Label(root, text=f"Block {i + 1}\nFree: {block_size} KB", bg="white", font=("Courier", 12), width=25, height=4, relief="solid", borderwidth=2)
    label.pack(pady=2)
    block_labels.append(label)

# Memory Status Display
memory_status = tk.StringVar(value="\n".join(manager.memory_status()))
tk.Label(root, textvariable=memory_status, font=("Courier", 10), justify=tk.LEFT).pack(pady=10)

root.mainloop()
