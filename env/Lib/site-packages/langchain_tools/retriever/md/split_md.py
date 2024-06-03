def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    sections = []
    title_stack = []
    current_content = []

    for line in lines:
        if line.startswith('#'):
            # Found a title, determine its level
            level = len(line.split()[0])
            title = line.strip().split(' ', 1)[1]

            # Update the title stack to reflect the current title hierarchy
            if level <= len(title_stack):
                title_stack = title_stack[:level-1]
            title_stack.append(title)

            # Save the previous section if it exists
            if current_content:
                sections.append("\n".join(current_content))
                current_content = []

            # Start a new section with the hierarchical title
            hierarchical_title = " - ".join(title_stack)
            current_content.append(hierarchical_title)

        else:
            # Accumulate content for the current section
            current_content.append(line.strip())

    # Add the last section if any content is remaining
    if current_content:
        sections.append("\n".join(current_content))

    return sections

# # Usage example, assuming the markdown file is in the same directory as the script
# file_name = "leave_policy.md"
# script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, file_name)

# sections = parse_markdown(file_path)
# for section in sections:
#     print("-" * 80)
#     print(section)
