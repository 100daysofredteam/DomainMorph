import itertools
import csv
import socket
import tldextract
import os
import sys
from typing import List, Tuple
import whois


# Homoglyphs mapping
HOMOGLYPHS = {
    'a': ['@', '4'],
    'e': ['3'],
    'i': ['1', 'l'],
    'o': ['0'],
    'l': ['1', 'i'],
    's': ['5', '$'],
    'g': ['9'],
    'b': ['8'],
}

# Close TLDs (commonly confused or typo-squatted)
COMMON_TLDS = ['.com', '.co', '.net', '.org', '.info', '.biz', '.xyz', '.io']

def generate_typos(domain_name: str) -> List[str]:
    """
    Generate basic typos such as character swaps, missing characters, duplicated characters
    """
    variations = set()
    for i in range(len(domain_name)):
        # Character omission
        variations.add(domain_name[:i] + domain_name[i+1:])
        # Character duplication
        variations.add(domain_name[:i] + domain_name[i] + domain_name[i:])
        # Adjacent character swap
        if i < len(domain_name) - 1:
            swapped = list(domain_name)
            swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
            variations.add(''.join(swapped))
    return list(variations)

def generate_homoglyphs(domain_name: str) -> List[str]:
    """
    Replace characters in domain with homoglyphs
    """
    variations = set()
    for i, char in enumerate(domain_name):
        if char in HOMOGLYPHS:
            for glyph in HOMOGLYPHS[char]:
                variation = domain_name[:i] + glyph + domain_name[i+1:]
                variations.add(variation)
    return list(variations)

def generate_hyphenated(domain_name: str) -> List[str]:
    """
    Insert hyphen in various positions
    """
    variations = set()
    for i in range(1, len(domain_name)):
        variations.add(domain_name[:i] + '-' + domain_name[i:])
    return list(variations)

def generate_tld_variations(domain_name: str, original_tld: str) -> List[str]:
    """
    Generate the same domain name with different TLDs
    """
    tlds = [tld for tld in COMMON_TLDS if tld != original_tld]
    return [domain_name + tld for tld in tlds]

def is_domain_registered(domain: str) -> bool:
    """
    Checks if domain has any DNS records (basic check)
    """
    try:
        info = whois.whois(domain)
        if info.domain_name:
            return True
        else:
            return False
    except Exception:
        return False

def generate_variations_and_check(domain: str) -> List[Tuple[str, str]]:
    """
    Generate variations of the domain and check registration status
    """
    ext = tldextract.extract(domain)
    base = ext.domain
    original_tld = '.' + ext.suffix
    all_variants = set()

    all_variants.update(generate_typos(base))
    all_variants.update(generate_homoglyphs(base))
    all_variants.update(generate_hyphenated(base))

    domain_variants = []
    for variant in all_variants:
        # Add original TLD
        domain_variants.append(f"{variant}{original_tld}")
        # Add other TLDs
        domain_variants.extend(generate_tld_variations(variant, original_tld))

    checked = []
    for var in set(domain_variants):
        try:
            status = "Registered" if is_domain_registered(var) else "Not Registered"
            checked.append((var, status))
        except Exception as e:
            checked.append((var, f"Error: {str(e)}"))
    return checked

def save_to_csv(results: List[Tuple[str, str]], output_file: str):
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Domain Variation", "Registration Status"])
        writer.writerows(results)

def main():
    if len(sys.argv) != 2:
        print("Usage: python dommorph.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    print(f"[+] Generating domain variations for: {domain}")
    results = generate_variations_and_check(domain)

    output_file = f"domain_variations_{domain.replace('.', '_')}.csv"
    save_to_csv(results, output_file)
    print(f"[+] Results saved to {output_file}")

if __name__ == "__main__":
    main()
