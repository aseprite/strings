from pathlib import Path

project_root_dir = Path(__file__).parent


def load_ini(file_path: Path) -> dict[str, dict[str, str]]:
    with file_path.open('r', encoding='utf-8') as file:
        ini = {}

        curr_section = None
        for line_num, line in enumerate(file):
            line_num += 1
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue

            if line.startswith('[') and line.endswith(']'):
                section_name = line.removeprefix('[').removesuffix(']').strip()
                if section_name in ini:
                    curr_section = ini[section_name]
                else:
                    curr_section = {}
                    ini[section_name] = curr_section
            elif '=' in line:
                if curr_section is None:
                    raise Exception(f'[{file_path.name}][{line_num}] no section')
                tokens = line.split('=', 1)
                key = tokens[0].strip()
                value = tokens[1].strip()
                curr_section[key] = value
            else:
                raise Exception(f'[{file_path.name}][{line_num}] illegal line')

        return ini


def normalize_ini(
        old_ini: dict[str, dict[str, str]],
        src_ini: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    new_ini = {}

    for section_name, src_section in src_ini.items():
        section_name = section_name.strip()
        if section_name not in old_ini:
            continue
        old_section = old_ini[section_name]

        for key in src_section.keys():
            key = key.strip()
            if key not in old_section:
                continue
            value = old_section[key].strip()

            if section_name in new_ini:
                new_section = new_ini[section_name]
            else:
                new_section = {}
                new_ini[section_name] = new_section
            new_section[key] = value

    return new_ini


def save_ini(
        headers: list[str],
        ini: dict[str, dict[str, str]],
        file_path: Path,
):
    with file_path.open('w', encoding='utf-8') as file:
        for header in headers:
            header = header.strip()
            file.write(f'# {header}\n')

        for section_name, section in ini.items():
            if len(section) <= 0:
                continue
            section_name = section_name.strip()
            file.write(f'\n[{section_name}]\n')
            for key, value in section.items():
                key = key.strip()
                value = value.strip()
                file.write(f'{key} = {value}\n')


def main():
    headers = [
        'This work is licensed under the Creative Commons Attribution 4.0',
        'International License. To view a copy of this license, visit',
        'http://creativecommons.org/licenses/by/4.0/ or send a letter to',
        'Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.',
    ]
    en_ini = load_ini(project_root_dir.joinpath('en.ini'))

    for file_path in project_root_dir.iterdir():
        if file_path.suffix != '.ini':
            continue
        if file_path.name == 'en.ini':
            continue

        print(f'Start format: {file_path}')
        lang_ini = load_ini(file_path)
        lang_ini = normalize_ini(lang_ini, en_ini)
        save_ini(headers, lang_ini, file_path)


if __name__ == '__main__':
    main()
