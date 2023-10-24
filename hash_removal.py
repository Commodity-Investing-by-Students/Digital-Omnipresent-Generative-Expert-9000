def remove_hashes_from_requirements(input_file, output_file):
    with open(input_file, 'r') as input_f:
        with open(output_file, 'w') as output_f:
            for line in input_f:
                if not line.strip().startswith('--hash='):
                    output_f.write(line)

if __name__ == "__main__":
    input_file = 'requirements.txt'
    output_file = 'requirements_hashless.txt'
    remove_hashes_from_requirements(input_file, output_file)
    print(f"Hashes removed. Output saved to {output_file}")
