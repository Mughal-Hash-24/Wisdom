import os

root_dir = r"D:\WISDOM\WISDOM\10_University"
standard_folders = ["Assignments", "Exams", "Lectures", "Notes", "Quizzes", "Resources"]

def get_subject_name_from_toc(toc_filename):
    # T.O.C (SubjectName).md -> SubjectName
    if toc_filename.startswith("T.O.C (") and toc_filename.endswith(").md"):
        return toc_filename[7:-4]
    return None

def update_subject_toc(subject_dir, subject_name, toc_file_path):
    # Read the content
    with open(toc_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    changes_made = False
    
    for folder in standard_folders:
        folder_path = os.path.join(subject_dir, folder)
        if os.path.exists(folder_path):
            # Define new specific T.O.C filename
            # Handle "Subject_Template" or normal subjects
            # For brevity in graph, maybe "T.O.C (AI Notes)"
            # But subject name might be long. Let's use full subject name for uniqueness.
            
            # Special handling for names to make them pretty in graph
            # If Subject is "Artificial Intelligence", folder "Notes" -> "AI Notes"?
            # User asked for "T.O.C (root) etc".
            # Let's stick to "T.O.C (Subject Folder)" e.g., "T.O.C (Artificial Intelligence Notes)"
            
            sub_toc_name = f"T.O.C ({subject_name} {folder})"
            sub_toc_filename = f"{sub_toc_name}.md"
            sub_toc_path = os.path.join(folder_path, sub_toc_filename)
            
            # 1. Create the Sub-T.O.C file
            if not os.path.exists(sub_toc_path):
                # Calculate relative path back to parent
                # Parent is subject_dir.
                # Link to parent T.O.C
                parent_toc_name = os.path.basename(toc_file_path).replace('.md', '')
                
                # Construct relative link path from inside the subfolder
                # ../T.O.C (Subject)
                
                # Obsidian style absolute path is safer/easier usually? 
                # Or relative? Standard seems to be WikiLinks which find the file.
                # I'll use the unique filename in the link.
                
                # Icon mapping
                icon_map = {
                    "Assignments": "📝",
                    "Exams": "⚖️",
                    "Lectures": "🗣️",
                    "Notes": "📓",
                    "Quizzes": "❓",
                    "Resources": "📚"
                }
                icon = icon_map.get(folder, "📁")
                
                file_content = f"# {icon} {subject_name} {folder}\n\n"
                file_content += f"[[{subject_dir.replace(root_dir, '10_University').replace(os.sep, '/')}/{os.path.basename(toc_file_path)}|⬅️ Up to {subject_name}]]\n"
                
                with open(sub_toc_path, 'w', encoding='utf-8') as f_sub:
                    f_sub.write(file_content)
                print(f"Created: {sub_toc_path}")

            # 2. Update the Parent T.O.C link
            # Look for `[[folder]]` e.g., `[[Notes]]`
            # Replace with `[[path/to/T.O.C (Subject Folder)|folder]]`
            
            generic_link = f"[[{folder}]]"
            
            # Construct relative path for the link from the parent T.O.C location
            # subfolder/sub_toc_name
            # But standard Obsidian link can just be the filename if unique.
            # However, providing full path is explicit.
            # Path relative to vault root:
            vault_rel_path = os.path.join(subject_dir, folder, sub_toc_name).replace(r"D:\WISDOM\WISDOM\\", "").replace("\\", "/")
            
            # We assume the user's current T.O.C has simple `[[Notes]]` style links from my previous generation
            specific_link = f"[[{folder}/{sub_toc_name}|{folder}]]"
            
            if generic_link in new_content:
                new_content = new_content.replace(generic_link, specific_link)
                changes_made = True
    
    if changes_made:
        with open(toc_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {toc_file_path}")

# Walk through 10_University
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.startswith("T.O.C (") and filename.endswith(").md"):
            # Check if this is a Subject T.O.C (parent of the subfolders we care about)
            # It is a subject T.O.C if it has the standard subfolders inside its directory
            is_subject_node = False
            for sf in standard_folders:
                if os.path.exists(os.path.join(dirpath, sf)):
                    is_subject_node = True
                    break
            
            if is_subject_node:
                subject_name = get_subject_name_from_toc(filename)
                # Avoid recursively processing the sub-TOCs we just created (names have spaces usually, but let's be safe)
                # Subject names: "Artificial Intelligence" -> T.O.C (Artificial Intelligence).md
                # Sub names: "Artificial Intelligence Notes" -> T.O.C (Artificial Intelligence Notes).md
                # We only want to process the Subject T.O.C, not the child ones.
                # My logic: "if it has standard subfolders inside its directory". 
                # The subfolders (Notes) do NOT have subfolders (Notes/Notes), so this check works.
                
                print(f"Processing Subject: {subject_name} in {dirpath}")
                update_subject_toc(dirpath, subject_name, os.path.join(dirpath, filename))