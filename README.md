# Vulnerable LLM Single Page Web App

## Vulnerability Coverage of OWASP 2023 LLM

### LLM01: Prompt Injection
Available through the message summarizer, where the messages are passed back from the tool without sanitization.

### LLM02: Insecure Output Handling - TODO
This will be available through the unsanitized handling of LLM response via the message summarizer, using dangerouslySetHTML.

### LLM03: Training Data Poisoning - TODO
Will be implemented through insecure RAG entries, as a form of "Send Feedback to The LLM" feature.

### LLM04: Model Denial of Service
No safeguards exist against mass requests to the /chat endpoint.

### LLM05: Supply Chain - TODO
Will use an intentionally vulnerable version of a python package.


### LLM06: Sensitive Information Disclosure
Implemented through the non-filtered message summary response, where it includes private messages.

### LLM07: Insecure Plugin Design
Command injection vulnerability in model info tool, will also implement user information access through raw sql query, to enable SQL injection.

### LLM08: Excessive Agency - TODO
Planned to be implemented by enabling LLM to read the "privacy statement" on the website, but will have the ability to modify the statement as well.

### LLM09: Overreliance
This is low-priority right now. Maybe I can implement this by enabling a "post summary message" tool, where the LLM gathers recent messages and posts a message claiming that they were from real authorative sources.

### LLM10: Model Theft
This is already implemented since there is no safeguard against usage of this model without logging in, or no rate limits.

## Vulnerability Coverage of OWASP 2025 LLM
Only the vulnerabilities not covered by the 2023.

### LLM07: System Prompt Leakage - TODO

### LLM08: Vector and Embedding Weakness

### LLM09: Misinformation

### LLM10: Unbounded Consumption
Maybe a fake wallet that decreases in funds every time a "request" is performed by the LLM.

