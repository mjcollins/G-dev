import json
from typing import Dict, Any

class MemoryManager:
    def __init__(self, storage_file: str = 'memory.json'):
        self.storage_file = storage_file
        self.memory: Dict[str, Any] = self.load_memory()

    def load_memory(self) -> Dict[str, Any]:
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_memory(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def store(self, key: str, value: Any) -> str:
        self.memory[key] = value
        self.save_memory()
        return f"Stored '{key}' in memory."

    def retrieve(self, key: str) -> str:
        if key in self.memory:
            return f"{key}: {self.memory[key]}"
        else:
            return f"'{key}' not found in memory."

    def list_keys(self) -> str:
        if self.memory:
            return "Memory keys:\n" + "\n".join(self.memory.keys())
        else:
            return "Memory is empty."

    def delete(self, key: str) -> str:
        if key in self.memory:
            del self.memory[key]
            self.save_memory()
            return f"Deleted '{key}' from memory."
        else:
            return f"'{key}' not found in memory."

    def handle_command(self, command: str) -> str:
        parts = command.split(maxsplit=2)
        if len(parts) < 2:
            return "Invalid memory command. Use 'store', 'retrieve', 'list', or 'delete'."
        
        operation = parts[0]
        
        if operation == "store" and len(parts) == 3:
            return self.store(parts[1], parts[2])
        elif operation == "retrieve" and len(parts) == 2:
            return self.retrieve(parts[1])
        elif operation == "list" and len(parts) == 1:
            return self.list_keys()
        elif operation == "delete" and len(parts) == 2:
            return self.delete(parts[1])
        else:
            return "Invalid memory operation. Use 'store', 'retrieve', 'list', or 'delete'."