import sys
import os
import subprocess

def patch_file(file_path, search_str, replace_str):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return False

    with open(file_path, 'r') as f:
        content = f.read()

    if search_str not in content:
        print(f"Error: Search string not found in {file_path}.")
        print("Search string start snippet:", repr(search_str[:50]))
        return False

    new_content = content.replace(search_str, replace_str)

    # Syntax validation for Javascript files
    if file_path.endswith('.js'):
        # Use .js extension for node --check compatibility
        temp_file = file_path + ".transcendent_check.js"
        with open(temp_file, 'w') as f:
            f.write(new_content)

        try:
            # Use node --check for syntax validation
            subprocess.run(['node', '--check', temp_file], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Syntax validation failed for proposed change to {file_path}.")
            print(e.stderr.decode())
            os.remove(temp_file)
            return False
        except FileNotFoundError:
            print("Warning: 'node' not found, skipping syntax validation.")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    with open(file_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully patched {file_path}.")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python definitive_transcendent_patch.py <file_path> <search_file> <replace_file>")
        sys.exit(1)

    target_path = sys.argv[1]
    search_path = sys.argv[2]
    replace_path = sys.argv[3]

    try:
        with open(search_path, 'r') as f:
            search_str = f.read()
        with open(replace_path, 'r') as f:
            replace_str = f.read()
    except Exception as e:
        print(f"Error reading patch files: {e}")
        sys.exit(1)

    if patch_file(target_path, search_str, replace_str):
        sys.exit(0)
    else:
        sys.exit(1)
