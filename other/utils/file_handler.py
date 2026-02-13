import gzip
import re
import json

class FileHandler:
    def __init__(self):
        self.content = ""
        self.file_path = None
    def load_file(self, file_path):
        self.file_path = file_path
        with gzip.open(file_path, "rb") as f:
            self.content = f.read().decode("utf-8", errors="ignore")
    def save_file(self, file_path):
        with gzip.open(file_path, "wb") as f:
            f.write(self.content.encode("utf-8"))
    def get_save_name(self):
        match = re.search(r'"name":"(.*?)"', self.content)
        return match.group(1) if match else "unknown"
    def set_save_name(self, name):
        self.content = re.sub(r'"name":"(.*?)"', f'"name":"{name}"', self.content, count=1)
    def get_crafts(self):
        crafts = []
        text_matches = list(re.finditer(r'"text":"(.*?)"', self.content))
        for match in text_matches:
            text_value = match.group(1)
            start = self.content.rfind("{", 0, match.start())
            end = self.content.find("}", match.end())
            if start == -1 or end == -1:
                continue
            block = self.content[start:end+1]
            id_match = re.search(r'"id":(\d+)', block)
            emoji_match = re.search(r'"emoji":"(.*?)"', block)
            craft_id = int(id_match.group(1)) if id_match else 0
            emoji_value = emoji_match.group(1) if emoji_match else "❓"
            crafts.append({
                'id': craft_id,
                'text': text_value,
                'emoji': emoji_value
            })
        return crafts
    def get_craft_by_id(self, craft_id):
        crafts = self.get_crafts()
        for craft in crafts:
            if craft['id'] == craft_id:
                return craft
        return None
    def add_craft(self, name, emoji, craft_id=None):
        if craft_id is None:
            all_ids = [int(m.group(1)) for m in re.finditer(r'"id":(\d+)', self.content)]
            craft_id = str(max(all_ids) + 1) if all_ids else "0"
        insert_pos = self.content.rfind("]}")
        if insert_pos == -1:
            raise ValueError("Could not find end of crafts array (]}).")
        addition = f',{{"id":{craft_id},"text":"{name}","emoji":"{emoji}"}}'
        self.content = self.content[:insert_pos] + addition + self.content[insert_pos:]
    def update_craft(self, craft_id, name, emoji):
        pattern = rf'{{"id":{craft_id},"text":".*?","emoji":".*?"}}'
        match = re.search(pattern, self.content)
        if not match:
            raise ValueError(f"Craft with ID {craft_id} not found")
        new_block = f'{{"id":{craft_id},"text":"{name}","emoji":"{emoji}"}}'
        self.content = self.content[:match.start()] + new_block + self.content[match.end():]
    def delete_craft(self, craft_id):
        pattern = rf',?{{"id":{craft_id},"text":".*?","emoji":".*?"}}'
        match = re.search(pattern, self.content)
        if not match:
            raise ValueError(f"Craft with ID {craft_id} not found")
        start = match.start()
        end = match.end()
        if self.content[start] == ',':
            self.content = self.content[:start] + self.content[end:]
        else:
            if end < len(self.content) and self.content[end] == ',':
                end += 1
            self.content = self.content[:start] + self.content[end:]
