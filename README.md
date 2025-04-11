# Domain Morph
## Objective
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


## Explanation of the Code

#### Homoglyphs Dictionary:
This dictionary holds mappings of characters to their visually similar counterparts. For example, "a" can be replaced with "а" (Cyrillic 'a') or "4" to create domain variations.

#### Domain Variation Generation:
The generate_variations_and_check function takes the base domain name and produces several types of variations:

    - Misspellings: By replacing each character in the domain with a random homoglyph.
    - Homoglyphs: For each character in the domain that has homoglyphs, generate a variation.
    - Hyphen Variations: Create variants with hyphens between sections of the domain.
    - Alternative TLDs: Check for popular alternative TLDs like .co, .net, etc.

#### Domain Registration Check:
The is_domain_registered function sends a simple HTTP request to a WHOIS service and checks if the domain is registered.

#### CSV Output:
Results are saved in a CSV file with the generated domain and its registration status.

#### Rate Limiting:
A sleep of 1 second is implemented between requests to avoid hammering the WHOIS servers, which may cause rate-limiting or blocking.

## Example Usage

Install the required Python modules first:
```  
   python3 -m pip install -r requirements.txt
```

Run the script with the following command to generate domain variations for xyz.com:

```  
   python3 domainMorph.py xyz.com
```

This will generate domain variations like xzy.com, xyz.co, and others, then check if they are registered and save the results in domain_variations.csv.

### CSV Output Example:

    Generated Domain, Registration Status
    xzy.com, Registered
    xyz.co, Unregistered
    xy-z.com, Unregistered
    ...
## Red Team Usecase

In a red-team engagement, this tool can be used to identify potential typosquat domain names against a target organization. For example, if the organization uses the domain xyz.com, you can run this tool to see if similar domain names like xyz.net or xzy.com are available for registration. If they are registered, it could indicate that an adversary might be using them for phishing or other malicious purposes.

The results can be used to inform mitigation strategies such as blocking the identified domains or alerting the organization to the risk.
