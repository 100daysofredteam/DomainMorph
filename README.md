# Domain Morph
## Objective:
This tool is designed to assist red teams in conducting domain variation attacks, commonly known as "typosquatting" or "domain name squatting," where they generate variations of a given domain name. These variations could include:

    Misspellings (e.g., xyz.com -> xzy.com).

    Homoglyphs (e.g., using visually similar characters like "0" for "o" or "l" for "1").

    Shortened domain names.

    Variations with hyphens or other common alterations.

The tool will also check if these domains are registered and log the result in a CSV file, which can be used for further analysis.
### Tool Structure

    Input: A domain name to generate variations.

    Output: A CSV file containing the generated domain variations along with their registration status (whether the domain is registered or not).

The tool is fully cross-platform, works on Windows, Linux, and macOS.


## Explanation of the Code:

    Homoglyphs Dictionary:
    This dictionary holds mappings of characters to their visually similar counterparts. For example, "a" can be replaced with "а" (Cyrillic 'a') or "4" to create domain variations.

    Domain Variation Generation:
    The generate_variations function takes the base domain name and produces several types of variations:

        Misspellings: By replacing each character in the domain with a random homoglyph.

        Homoglyphs: For each character in the domain that has homoglyphs, generate a variation.

        Shortened Forms: A short version of the domain, like using the first three characters.

        Hyphen Variations: Create variants with hyphens between sections of the domain.

        Alternative TLDs: Check for popular alternative TLDs like .co, .net, etc.

    Domain Registration Check:
    The check_domain_registration function sends a simple HTTP request to a WHOIS service and checks if the domain is registered.

    CSV Output:
    Results are saved in a CSV file with the generated domain and its registration status.

    Rate Limiting:
    A sleep of 1 second is implemented between requests to avoid hammering the WHOIS servers, which may cause rate-limiting or blocking
