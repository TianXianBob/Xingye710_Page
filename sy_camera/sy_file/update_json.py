import os
import json
import glob

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    modified = False

    # 0. Add version to data
    data_obj = data.get('data')
    if isinstance(data_obj, dict):
        if data_obj.get('version') != "0.0.1":
            data_obj['version'] = "0.0.1"
            modified = True
    else:
        print(f"Skipping version update for {file_path}: 'data' is not a dict")

    # Navigate to rects
    # Structure seems to be data -> canvas -> rects
    canvas = data.get('data', {}).get('canvas')
    if not canvas:
        # Try finding canvas in root if structure is different, but based on exploration it's data->canvas
        # If strict structure is required:
        print(f"Skipping {file_path}: 'canvas' not found in data")
        return

    rects = canvas.get('rects', [])
    if not isinstance(rects, list):
        print(f"Skipping {file_path}: 'rects' is not a list")
        return

    for rect in rects:
        # 1. Add layoutMode: 1 to rect
        if rect.get('layoutMode') != 1:
            rect['layoutMode'] = 1
            modified = True
        
        # 2. Add layoutMode: 0 to textPieces inside rect
        text_pieces = rect.get('textPieces', [])
        if isinstance(text_pieces, list):
            for tp in text_pieces:
                if tp.get('layoutMode') != 0:
                    tp['layoutMode'] = 0
                    modified = True
        
        # 3. Add layoutMode: 0 to imagePieces inside rect
        image_pieces = rect.get('imagePieces', [])
        if isinstance(image_pieces, list):
            for ip in image_pieces:
                if ip.get('layoutMode') != 0:
                    ip['layoutMode'] = 0
                    modified = True
        
        # 4. Handle cells
        cells = rect.get('cells', [])
        if isinstance(cells, list):
            for cell in cells:
                # cell -> textPiece -> layoutMode: 1
                text_piece = cell.get('textPiece')
                if isinstance(text_piece, dict):
                    if text_piece.get('layoutMode') != 1:
                        text_piece['layoutMode'] = 1
                        modified = True
                
                # cell -> imagePiece -> layoutMode: 0
                image_piece = cell.get('imagePiece')
                if isinstance(image_piece, dict):
                    if image_piece.get('layoutMode') != 0:
                        image_piece['layoutMode'] = 0
                        modified = True

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {file_path}")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
    else:
        print(f"No changes needed for {file_path}")

def main():
    root_dir = '/Users/bob/Xingye710_Page/sy_camera/sy_file'
    # Find all directories starting with sy_
    dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and d.startswith('sy_')]
    
    for d in dirs:
        dir_path = os.path.join(root_dir, d)
        content_json_path = os.path.join(dir_path, 'content.json')
        
        if os.path.exists(content_json_path):
            process_file(content_json_path)
        else:
            # print(f"No content.json in {d}")
            pass

if __name__ == '__main__':
    main()
